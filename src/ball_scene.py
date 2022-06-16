from typing import List, Optional

from PyQt6.QtCore import QPointF, QTimer, Qt
from PyQt6.QtWidgets import QGraphicsScene
from selecting_rect import SelectingRect
from ball import Ball

DEFAULT_PEN_WIDTH = 0
SELECTED_PEN_WIDTH = 2


class BallScene(QGraphicsScene):
    def __init__(
            self,
            frame_per_second: int,
            balls: List[Ball],
            selecting_rect: SelectingRect,
            widget: "BallWidget",
    ):
        super().__init__()
        self._mouse_position: Optional[QPointF] = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.one_timer_tick)
        self.timer.start(round(1000 / frame_per_second))
        self._balls: List[Ball] = balls
        self._selected_balls: List[Ball] = []
        self._selecting_rect: SelectingRect = selecting_rect
        self._widget = widget

        for ball in balls:
            ball.add_ball_to_scene(self)

        selecting_rect.add_rect_to_scene(self)

    def key_press_event(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._widget.close()
        if event.key() == Qt.Key.Key_Space:
            for ball in self._selected_balls:
                jump = ball.calculate_jump()
                if jump is not None:
                    jump_shift = ball.pos() + ball.calculate_jump()
                    ball.setPos(jump_shift)
        self.update()

    def mouse_move_event(self, event):
        if not self._selecting_rect.is_none():
            self._selecting_rect.expand_rect(event.pos())
        self._mouse_position = QPointF(event.pos())
        self.update()

    def mouse_release_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._selecting_rect.is_small():
                for ball in self._balls:
                    if ball.is_clicked(mouse_position=QPointF(event.pos())):
                        self._selected_balls = [ball]
            else:
                self._selected_balls = self._selecting_rect.filter_selected_balls(self._balls)
        for ball in self._balls:
            ball.draw_selected(ball=ball, selected_balls=self._selected_balls)
        self.update()
        self._selecting_rect.clear_rect()

    def mouse_press_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self._selecting_rect.start_rect(event.pos())
        if event.buttons() == Qt.MouseButton.RightButton:
            if self._selected_balls is not None:
                for ball in self._selected_balls:
                    ball.set_center_target(center_target=QPointF(event.pos()))

    def one_timer_tick(self):
        for ball in self._balls:
            shift = ball.calculate_shift_on_tick()
            if shift is not None:
                new_pos = ball.pos() + shift
                ball.setPos(new_pos)
