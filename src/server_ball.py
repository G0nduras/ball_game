import math
from typing import Optional
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QVector2D
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene
from balls_positions import BallPosition

DEFAULT_PEN_WIDTH = 0
SELECTED_PEN_WIDTH = 2


class ServerBall(QGraphicsEllipseItem):
    def __init__(
            self,
            x: int,
            y: int,
            radius: int,
            resistance_alpha: float,
            density: float,
            thrust_force_module: float,
            jump_impulse_module: float,
    ):
        super().__init__(-radius, - radius, radius * 2, radius * 2)
        self.setPos(QPointF(x, y))
        self._radius = radius
        self._velocity: QVector2D = QVector2D(0, 0)
        self._center_target: Optional[QPointF] = None
        self._mass = 4 / 3 * math.pi * radius ** 3 * density
        self._resistance_alpha = resistance_alpha
        self._density = density
        self._thrust_force_module = thrust_force_module
        self._impulse: QVector2D = QVector2D(0, 0)
        self._jump_impulse_module = jump_impulse_module

    def add_ball_to_scene(self, scene: QGraphicsScene):
        scene.addItem(self)

    def set_center_target(self, center_target: QPointF):
        self._center_target = center_target

    def calculate_moving_direction(self) -> Optional[QVector2D]:
        if self._center_target is None:
            return None
        from_ball_to_target = QVector2D(self._center_target - self.scenePos())
        return from_ball_to_target.normalized()

    def add_impulse(self, impulse: QVector2D):
        self._impulse += impulse

    def calculate_thrust_force(self) -> QVector2D:
        moving_direction = self.calculate_moving_direction()
        if moving_direction is not None:
            thrust_force = self._thrust_force_module * moving_direction
            return thrust_force
        else:
            return QVector2D(0, 0)

    def calculate_friction_force(self) -> QVector2D:
        friction_force = - self._resistance_alpha * self._radius * self._velocity
        return friction_force

    def calculate_sum_force(self) -> QVector2D:
        force = self.calculate_thrust_force() + self.calculate_friction_force()
        force += self._impulse
        self._impulse = QVector2D(0, 0)
        return force

    def get_position(self) -> BallPosition:
        return BallPosition(float(self.pos().x()), float(self.pos().y()))

    def jump(self, ball):
        if ball._center_target is not None:
            impulse = self.calculate_moving_direction() * ball._jump_impulse_module
            ball.add_impulse(impulse)
