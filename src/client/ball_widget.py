from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from client_scene import ClientScene


class BallWidget(QGraphicsView):
    client_is_disconnected = pyqtSignal()

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
            self.client_is_disconnected.emit()
            self.close()
        if self._scene is not None:
            self._scene.key_press_event(event)

    def mouseMoveEvent(self, event):
        if self._scene is not None:
            self._scene.mouse_move_event(event)

    def mouseReleaseEvent(self, event):
        if self._scene is not None:
            self._scene.mouse_release_event(event)

    def mousePressEvent(self, event):
        if self._scene is not None:
            self._scene.mouse_press_event(event)
