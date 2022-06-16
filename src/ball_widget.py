from typing import List
from PyQt6.QtWidgets import QGraphicsView
from ball import Ball
from ball_scene import BallScene
from selecting_rect import SelectingRect


class BallWidget(QGraphicsView):
    def __init__(
            self,
            balls: List[Ball],
            selecting_rect: SelectingRect,
            frame_per_second: int,
    ):
        super().__init__()
        self._scene = BallScene(
            balls=balls,
            selecting_rect=selecting_rect,
            frame_per_second=frame_per_second,
            widget=self,
        )
        self.setScene(self._scene)

    def keyPressEvent(self, event):
        self._scene.key_press_event(event)

    def mouseMoveEvent(self, event):
        self._scene.mouse_move_event(event)

    def mouseReleaseEvent(self, event):
        self._scene.mouse_release_event(event)

    def mousePressEvent(self, event):
        self._scene.mouse_press_event(event)
