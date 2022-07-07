from typing import List, Dict
from PyQt6.QtCore import QPointF
from client_player import ClientPlayer


class BallPosition:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def to_q_point_f(self):
        return QPointF(self.x, self.y)


class BallsPositions:
    def __init__(self, player_id_2_ball_position: Dict[int, List[BallPosition]]):
        self.player_id_2_ball_position: Dict[int, List[BallPosition]] = player_id_2_ball_position

    @staticmethod
    def from_players(players: List["ServerPlayer"]) -> "BallsPositions":
        return BallsPositions(player_id_2_ball_position={
            player.players_id: [ball.get_position() for ball in player.balls]
            for player in players
        })

    def set_to_players(self, players: List[ClientPlayer]):
        assert len(players) == len(self.player_id_2_ball_position)
        for player in players:
            ball_positions_to_set = self.player_id_2_ball_position[player.players_id]
            assert len(ball_positions_to_set) == len(player.balls)
            for ball, ball_position in zip(player.balls, ball_positions_to_set):
                ball.setPos(ball_position.to_q_point_f())
