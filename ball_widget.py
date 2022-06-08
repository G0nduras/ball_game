from typing import Optional, List
from PyQt6.QtCore import Qt, QTimer, QPointF, QRect
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush

from ball import Ball
from selecting_rect import SelectingRect

DEFAULT_PEN_WIDTH = 0
SELECTED_PEN_WIDTH = 2


class BallWidget(QWidget):
    def __init__(
            self,
            width: float,
            height: float,
            step: float,
            frame_per_second: int,
            balls: List[Ball],
            selecting_rect: SelectingRect,
    ):
        super().__init__()
        self._width: float = width
        self._height: float = height
        self._step: float = step
        self._mouse_position: Optional[QPointF] = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.one_timer_tick)
        self.timer.start(round(1000 / frame_per_second))
        self._balls: List[Ball] = balls
        self._selected_balls: List[Ball] = []
        self._selecting_rect: SelectingRect = selecting_rect

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self._selecting_rect.is_none():
            pen = QPen()
            pen.setWidth(0)
            painter.setPen(pen)
            painter.setBrush(QBrush(QColor(0, 200, 0, 50), Qt.BrushStyle.SolidPattern))
            painter.drawRect(self._selecting_rect.get_rect())
        for ball in self._balls:
            if ball not in self._selected_balls:
                ball.draw(painter=painter, mouse_position=self._mouse_position, hover_pen_width=DEFAULT_PEN_WIDTH)
        for ball in self._selected_balls:
            ball.draw(painter=painter, mouse_position=self._mouse_position, hover_pen_width=SELECTED_PEN_WIDTH)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            for ball in self._selected_balls:
                jump_shift = ball.calculate_jump()
                ball.move(jump_shift)
        self.update()

    def mouseMoveEvent(self, event):
        if not self._selecting_rect.is_none():
            self._selecting_rect.expand_rect(event.pos())
        self._mouse_position = QPointF(event.pos())
        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._selecting_rect.is_small():
                for ball in self._balls:
                    if ball.is_clicked(mouse_position=QPointF(event.pos())):
                        self._selected_balls = [ball]
            else:
                self._selected_balls = self._selecting_rect.filter_selected_balls(self._balls)
        self._selecting_rect.clear_rect()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self._selecting_rect.start_rect(event.pos())
        if event.buttons() == Qt.MouseButton.RightButton:
            if self._selected_balls is not None:
                for ball in self._selected_balls:
                    ball.set_center_target(center_target=QPointF(event.pos()))

    def one_timer_tick(self):
        for ball in self._balls:
            shift = ball.calculate_shift_on_tick()
            ball.move(shift)
        self.update()

