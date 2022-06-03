import sys
from typing import Optional, List
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter

from ball import Ball


class BallWidget(QWidget):
    def __init__(
            self,
            width: float,
            height: float,
            step: float,
            frame_per_second: int,
            balls: List[Ball],
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
        self._select_ball = None

    def paintEvent(self, event):
        painter = QPainter(self)
        for ball in self._balls:
            ball.draw(painter=painter, mouse_position=self._mouse_position)

    def mouseMoveEvent(self, event):
        self._mouse_position = QPointF(event.pos())
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.MouseButton.RightButton:
            for ball in self._balls:
                if ball.is_clicked(mouse_position=QPointF(event.pos())):
                    self._select_ball = ball

        if event.buttons() == Qt.MouseButton.LeftButton:
            if self._select_ball is not None:
                self._select_ball.set_center_target(center_target=QPointF(event.pos()))

    def one_timer_tick(self):
        for ball in self._balls:
            shift = ball.calculate_shift2()
            ball.move(shift)
        self.update()

