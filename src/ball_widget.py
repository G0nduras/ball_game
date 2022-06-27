from typing import List
from PyQt6.QtWidgets import QGraphicsView
from ball import Ball
from client_scene import ClientScene
from selecting_rect import SelectingRect


class BallWidget(QGraphicsView):
    def __init__(
            self,
            balls: List[Ball],
    ):
        super().__init__()
        self._scene = ClientScene(
            balls=balls,
            exit_function=self.close,
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
