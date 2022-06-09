from typing import Optional
from PyQt6.QtCore import Qt, QPointF, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QVector2D
from PyQt6.QtWidgets import QGraphicsEllipseItem


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
        super().__init__(x, y, radius, radius)
        self._default_color = default_color
        self._hover_color = hover_color
        self._radius = radius
        self._speed = speed
        self._jump_len = jump_len
        self._center_target: Optional[QPointF] = None

    def intersects_with_rect(self, rect: QRect) -> bool:
        return rect.contains(self.pos().toPoint())

    def set_center_target(self, center_target: QPointF):
        self._center_target = center_target

    def _get_circle_color(self, mouse_position: QPointF) -> str:
        if mouse_position is None:
            return self._default_color

        from_circle_to_mouse = QVector2D(self.pos() - mouse_position)
        if from_circle_to_mouse.length() < self._radius:
            return self._hover_color
        else:
            return self._default_color

    def calculate_moving_direction(self) -> Optional[QVector2D]:
        if self._center_target is None:
            return None
        from_ball_to_target = QVector2D(self._center_target - self.pos())
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
        vector = QVector2D(self.pos() - mouse_position)
        return vector.length() <= self._radius
