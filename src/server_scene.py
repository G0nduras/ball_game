from typing import List
from math import sqrt
from PyQt6.QtCore import QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QVector2D
from PyQt6.QtWidgets import QGraphicsScene
from server_ball import ServerBall
from balls_positions import BallsPositions
from targets_for_selected_balls import TargetsForBallsMessage
from server_player import ServerPlayer
from jump_message import JumpMessage


MIN_TARGET_DISTANCE = 2


class ServerScene(QGraphicsScene):
    MS_IN_S = 1000
    set_pos_signal = pyqtSignal(BallsPositions)

    def __init__(
            self,
            server_players: List[ServerPlayer],
            frame_per_second: int,
    ):
        super().__init__()
        self._frame_per_second = frame_per_second
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.start(round(ServerScene.MS_IN_S / frame_per_second))
        self._server_players: List[ServerPlayer] = server_players

        for player in server_players:
            for ball in player.balls:
                ball.add_ball_to_scene(self)

    @pyqtSlot(JumpMessage)
    def set_jump(self, jump_message: JumpMessage):
        player_id = jump_message.player_indices
        indices = jump_message.ball_indices
        player: ServerPlayer = self._server_players[player_id]
        for i in indices:
            player.balls[i].jump()

    @pyqtSlot(TargetsForBallsMessage)
    def set_target_for_selected_balls(self, ball_indices_and_target: TargetsForBallsMessage):
        ball_indices = ball_indices_and_target.indices
        target = ball_indices_and_target.position
        player_id = ball_indices_and_target.player_id
        player: ServerPlayer = self._server_players[player_id]
        for i in ball_indices:
            player.balls[i].set_center_target(center_target=target.to_q_point_f())

    def _list_all_balls(self) -> List[ServerBall]:
        return [
            ball
            for player in self._server_players
            for ball in player.balls
        ]

    def _calculate_crash_impulses(self):
        balls = self._list_all_balls()
        for index_1 in range(0, len(balls)):
            for index_2 in range(index_1 + 1, len(balls)):
                ball_1 = balls[index_1]
                ball_2 = balls[index_2]
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
        for player in self._server_players:
            for ball in player.balls:
                force = ball.calculate_sum_force()
                assert isinstance(force, QVector2D), type(force)
                distance_to_target = ball.distance_to_target()
                ball.move_with_force(force)
                if (distance_to_target is not None) and (distance_to_target < MIN_TARGET_DISTANCE):
                    ball.clear_target()

    def on_timer_tick(self):
        self._calculate_crash_impulses()
        self._update_ball_positions()
        self.set_pos_signal.emit(BallsPositions.from_players(self._server_players))
