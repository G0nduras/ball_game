from typing import List
from math import sqrt
from PyQt6.QtCore import QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QVector2D
from PyQt6.QtWidgets import QGraphicsScene
from server_ball import ServerBall
from balls_positions import BallsPositions, BallPosition

MIN_TARGET_DISTANCE = 2


class ServerScene(QGraphicsScene):
    MS_IN_S = 1000
    on_timer_tick_signal = pyqtSignal(BallsPositions)

    def __init__(
            self,
            balls: List[ServerBall],
            frame_per_second: int,
    ):
        super().__init__()
        self._frame_per_second = frame_per_second
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.start(round(ServerScene.MS_IN_S / frame_per_second))
        self._balls: List[ServerBall] = balls

        for ball in balls:
            ball.add_ball_to_scene(self)

    @pyqtSlot(list)
    def set_jump(self, ball_indices: List[int]):
        for i in ball_indices:
            self._balls[i].jump()

    @pyqtSlot(list, BallPosition)
    def set_target_for_selected_balls(self, ball_indices: List[int], target: BallPosition):
        for i in ball_indices:
            self._balls[i].set_center_target(center_target=target.to_q_point_f())

    def _calculate_crash_impulses(self):
        for index_1 in range(0, len(self._balls)):
            for index_2 in range(index_1 + 1, len(self._balls)):
                ball_1 = self._balls[index_1]
                ball_2 = self._balls[index_2]
                if ball_1.collides_with(ball_2):
                    ball_to_ball = QVector2D(ball_1.pos() - ball_2.pos())
                    colliding_direction = ball_to_ball / ball_to_ball.length()
                    init_impulse_1 = ball_1.impulse()
                    init_impulse_2 = ball_2.impulse()
                    impulse_projection_1 = QVector2D.dotProduct(init_impulse_1, colliding_direction)
                    impulse_projection_2 = QVector2D.dotProduct(init_impulse_2, colliding_direction)
                    m1 = ball_1.mass
                    m2 = ball_2.mass
                    v_1 = impulse_projection_1 / m1
                    v_2 = impulse_projection_2 / m2
                    e_0 = (m1 * (v_1 ** 2)) / 2 + (m2 * (v_2 ** 2)) / 2
                    p_0 = m1 * v_1 + m2 * v_2
                    discriminant = sqrt(m1 * m2) * sqrt(2 * e_0 * (m1 + m2) - p_0 ** 2)
                    final_velocity_projection_1 = (p_0 * m1 + discriminant) / (m1 * (m1 + m2))
                    final_velocity_projection_2 = (p_0 * m2 - discriminant) / (m2 * (m1 + m2))
                    delta_impulse_1 = (m1 * final_velocity_projection_1 - impulse_projection_1) * colliding_direction
                    delta_impulse_2 = (m2 * final_velocity_projection_2 - impulse_projection_2) * colliding_direction
                    ball_1.add_impulse(delta_impulse_1)
                    ball_2.add_impulse(delta_impulse_2)

    def _update_ball_positions(self):
        for ball in self._balls:
            force = ball.calculate_sum_force()
            assert isinstance(force, QVector2D), type(force)
            distance_to_target = ball.distance_to_target()
            ball.move_with_force(force)
            if (distance_to_target is not None) and (distance_to_target < MIN_TARGET_DISTANCE):
                ball.clear_target()

    def on_timer_tick(self):
        self._calculate_crash_impulses()
        self._update_ball_positions()
        self.on_timer_tick_signal.emit(BallsPositions.from_balls(self._balls))
