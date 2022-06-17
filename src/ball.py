from typing import Optional
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QVector2D
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene

DEFAULT_PEN_WIDTH = 0
SELECTED_PEN_WIDTH = 2


class Ball(QGraphicsEllipseItem):
    def __init__(
            self,
            x: int,
            y: int,
            default_color: str,
            hover_color: str,
            radius: int,
            jump_len: float,
            mass: float,
            power: float,
            alpha: float,
    ):
        super().__init__(-radius, - radius, radius * 2, radius * 2)
        self.setPos(QPointF(x, y))
        self._default_color = default_color
        self._hover_color = hover_color
        self._radius = radius
        self._velocity: QVector2D = QVector2D(0, 0)
        self._jump_len = jump_len
        self._center_target: Optional[QPointF] = None
        self._mass = mass
        self._power = power
        self._alpha = alpha

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

    def set_center_target(self, center_target: QPointF):
        self._center_target = center_target

    def calculate_moving_direction(self) -> Optional[QVector2D]:
        if self._center_target is None:
            return None
        from_ball_to_target = QVector2D(self._center_target - self.scenePos())
        #if from_ball_to_target.length() < self._power:
        #    return None
        return from_ball_to_target.normalized()

    def calculate_jump(self) -> Optional[QPointF]:
        jump_direction: QVector2D = self.calculate_moving_direction()
        if jump_direction is None:
            return None
        return jump_direction.toPointF() * self._jump_len

    def get_force(self) -> QVector2D:
        force = QVector2D(0, 0)
        moving_direction = self.calculate_moving_direction()
        if moving_direction is not None:
            force += moving_direction * self._power
        force -= self._alpha * self._velocity
        return force

    def is_clicked(self, mouse_position: QPointF) -> bool:
        vector = QVector2D(self.scenePos() - mouse_position)
        return vector.length() <= self._radius
