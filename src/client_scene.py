from typing import List, Optional, Callable

from PyQt6.QtCore import QPointF, Qt, pyqtSlot, QRect
from PyQt6.QtWidgets import QGraphicsScene
from ball import Ball
from selecting_rect import SelectingRect
from balls_positions import BallsPositions
from server_scene import ServerScene


class ClientScene(QGraphicsScene):
    def __init__(
            self,
            balls: List[Ball],
            exit_function: Callable,
    ):
        super().__init__()

        self._server_scene = ServerScene(balls, frame_per_second=60, repulsive_mul=10000)
        self._server_scene.on_timer_tick_signal.connect(self.get_balls_position)

        self._mouse_position: Optional[QPointF] = None
        self._balls: List[Ball] = balls
        self._selected_balls: List[Ball] = []
        self._selecting_rect: SelectingRect = SelectingRect()
        self._exit_function = exit_function

        for ball in balls:
            ball.add_ball_to_scene(self)

        self._selecting_rect.add_rect_to_scene(self)

    def key_press_event(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._exit_function()
        if event.key() == Qt.Key.Key_Space:
            for ball in self._selected_balls:
                if ball._center_target is not None:
                    impulse = ball.calculate_moving_direction() * ball._impulse_score
                    ball.add_impulse(impulse)
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
                        break
                else:
                    self._selected_balls = []
            else:
                self._selected_balls = self._selecting_rect.filter_selected_balls(self._balls)
        for ball in self._balls:
            ball.set_draw_method(is_selected=ball in self._selected_balls)
        self.update()
        self._selecting_rect.clear_rect()

    def mouse_press_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self._selecting_rect.start_rect(event.pos())
        if event.buttons() == Qt.MouseButton.RightButton:
            if self._selected_balls is not None:
                for ball in self._selected_balls:
                    ball.set_center_target(center_target=QPointF(event.pos()))

    @pyqtSlot(BallsPositions)
    def get_balls_position(self, positions: BallsPositions):
        positions.set_to_balls(self._balls)
