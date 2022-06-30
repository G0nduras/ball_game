from PyQt6.QtCore import QPointF, Qt, QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QVector2D
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene

DEFAULT_PEN_WIDTH = 0
SELECTED_PEN_WIDTH = 2


class ClientBall(QGraphicsEllipseItem):
    def __init__(
            self,
            x: int,
            y: int,
            default_color: str,
            hover_color: str,
            radius: int,
    ):
        super().__init__(-radius, - radius, radius * 2, radius * 2)
        self.setPos(QPointF(x, y))
        self._default_color = default_color
        self._hover_color = hover_color
        self._radius = radius

    def add_ball_to_scene(self, scene: QGraphicsScene):
        pen = QPen()
        pen.setWidth(DEFAULT_PEN_WIDTH)
        self.setPen(pen)
        self.setBrush(QBrush(QColor(self._default_color), Qt.BrushStyle.SolidPattern))
        scene.addItem(self)

    def set_draw_method(self, is_selected: bool):
        if not is_selected:
            pen = QPen()
            pen.setWidth(DEFAULT_PEN_WIDTH)
            self.setPen(pen)
        else:
            pen = QPen()
            pen.setWidth(SELECTED_PEN_WIDTH)
            self.setPen(pen)

    def intersects_with_rect(self, rect: QRectF) -> bool:
        return rect.contains(self.scenePos())

    def is_clicked(self, mouse_position: QPointF) -> bool:
        vector = QVector2D(self.scenePos() - mouse_position)
        return vector.length() <= self._radius
