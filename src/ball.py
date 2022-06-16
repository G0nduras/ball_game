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
            speed: float,
            jump_len: float,
    ):
        super().__init__(0 - radius / 2, 0 - radius / 2, radius, radius)
        self.setPos(QPointF(x, y))
        self._default_color = default_color
        self._hover_color = hover_color
        self._radius = radius
        self._speed = speed
        self._jump_len = jump_len
        self._center_target: Optional[QPointF] = None

    def add_ball_to_scene(self, scene: QGraphicsScene):
        pen = QPen()
        pen.setWidth(DEFAULT_PEN_WIDTH)
        self.setPen(pen)
        self.setBrush(QBrush(QColor(self._default_color), Qt.BrushStyle.SolidPattern))
        scene.addItem(self)

    def draw_selected(self,  ball, selected_balls):
        if ball not in selected_balls:
            pen = QPen()
            pen.setWidth(DEFAULT_PEN_WIDTH)
            self.setPen(pen)
            self.setBrush(QBrush(QColor(self._default_color), Qt.BrushStyle.SolidPattern))
        if ball in selected_balls:
            pen = QPen()
            pen.setWidth(SELECTED_PEN_WIDTH)
            self.setPen(pen)
            self.setBrush(QBrush(QColor(self._hover_color), Qt.BrushStyle.SolidPattern))

    def intersects_with_rect(self, rect: QRectF) -> bool:
        return rect.contains(self.scenePos())

    def set_center_target(self, center_target: QPointF):
        self._center_target = center_target

    def calculate_moving_direction(self) -> Optional[QVector2D]:
        if self._center_target is None:
            return None
        from_ball_to_target = QVector2D(self._center_target - self.scenePos())
        if from_ball_to_target.length() < self._speed:
            return None
        return from_ball_to_target.normalized()

    def calculate_jump(self) -> Optional[QPointF]:
        jump_direction: QVector2D = self.calculate_moving_direction()
        if jump_direction is None:
            return None
        return jump_direction.toPointF() * self._jump_len

    def calculate_shift_on_tick(self) -> Optional[QPointF]:
        target_direction: QVector2D = self.calculate_moving_direction()
        if target_direction is None:
            return None
        return target_direction.toPointF() * self._speed

    def is_clicked(self, mouse_position: QPointF) -> bool:
        vector = QVector2D(self.scenePos() - mouse_position)
        return vector.length() <= self._radius
