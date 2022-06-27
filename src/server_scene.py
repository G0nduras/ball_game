from typing import List
from math import sqrt
from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtGui import QVector2D
from PyQt6.QtWidgets import QGraphicsScene
from ball import Ball
from balls_positions import BallsPositions

MIN_TARGET_DISTANCE = 2


class ServerScene(QGraphicsScene):
    MS_IN_S = 1000
    on_timer_tick_signal = pyqtSignal(BallsPositions)

    def __init__(
            self,
            balls: List[Ball],
            frame_per_second: int,
            repulsive_mul: int,
    ):
        super().__init__()
        self._frame_per_second = frame_per_second
        self._repulsive_mul = repulsive_mul
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.start(round(ServerScene.MS_IN_S / frame_per_second))
        self._balls: List[Ball] = balls

        for ball in balls:
            ball.add_ball_to_scene(self)

    def _calculate_crash_impulses(self):
        for index_1 in range(0, len(self._balls)):
            for index_2 in range(index_1 + 1, len(self._balls)):
                ball1 = self._balls[index_1]
                ball2 = self._balls[index_2]
                if QVector2D((ball1.pos() - ball2.pos())).length() < ball1._radius + ball2._radius:
                    mass1 = ball1._mass
                    mass2 = ball2._mass
                    velocity1 = ball1._velocity
                    velocity2 = ball2._velocity
                    ball_to_ball = QVector2D(ball1.pos() - ball2.pos())
                    p_1 = mass1 * velocity1
                    p_2 = mass2 * velocity2
                    projection_p1 = QVector2D.dotProduct(p_1, ball_to_ball) * ball_to_ball.length()
                    projection_p2 = QVector2D.dotProduct(p_2, ball_to_ball) * ball_to_ball.length()
                    v_1 = projection_p1 / mass1
                    v_2 = projection_p2 / mass2
                    e_0 = (mass1 * (v_1 ** 2)) / 2 + (mass2 * (v_2 ** 2)) / 2
                    p_0 = mass1 * v_1 + mass2 * v_2
                    discriminant = sqrt(mass1 * mass2) * sqrt(2 * e_0 * (mass1 + mass2) - p_0 ** 2)
                    projection_v_1 = (p_0 * mass1 + discriminant) / (mass1 * (mass1 + mass2))
                    projection_v_2 = (p_0 * mass2 - discriminant) / (mass2 * (mass1 + mass2))
                    d = ball_to_ball / ball_to_ball.length()
                    ball1.add_impulse((mass1 * projection_v_1 - mass1 * v_1) * d / self._repulsive_mul)
                    ball2.add_impulse((mass2 * projection_v_2 - mass2 * v_2) * d / self._repulsive_mul)

    def _update_ball_positions(self):
        for ball in self._balls:
            force = ball.calculate_sum_force()
            assert isinstance(force, QVector2D), type(force)
            acceleration = force / ball._mass
            # F = m*a
            ball._velocity += acceleration
            # V = a => DELTA_V = a * DELTA_t
            new_pos = ball.pos() + ball._velocity.toPointF()
            if ball._center_target is not None:
                shift = QVector2D(new_pos - ball._center_target)
                if shift.length() < MIN_TARGET_DISTANCE:
                    ball._center_target = None
            ball.setPos(new_pos)

    def on_timer_tick(self):
        self._calculate_crash_impulses()
        self._update_ball_positions()
        self.on_timer_tick_signal.emit(BallsPositions.from_balls(self._balls))
