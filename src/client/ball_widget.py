from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from client_scene import ClientScene


class BallWidget(QGraphicsView):
    def __init__(
            self,
    ):
        super().__init__()
        self._scene: Optional[QGraphicsScene] = None

    def set_scene(self, client_scene: ClientScene):
        self._scene = client_scene
        self.setScene(self._scene)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        self._scene.key_press_event(event)

    def mouseMoveEvent(self, event):
        self._scene.mouse_move_event(event)

    def mouseReleaseEvent(self, event):
        self._scene.mouse_release_event(event)

    def mousePressEvent(self, event):
        self._scene.mouse_press_event(event)
