from typing import List, Dict
from src.client.client_player import ClientPlayer
from src.network.ball_position import BallPosition


class BallsPositionsMessage:
    def __init__(self, player_id_2_ball_position: Dict[int, List[BallPosition]]):
        self.player_id_2_ball_position: Dict[int, List[BallPosition]] = player_id_2_ball_position

    @staticmethod
    def from_players(players: Dict[int, "ServerPlayer"]) -> "BallsPositionsMessage":
        return BallsPositionsMessage(player_id_2_ball_position={
            player.player_id: [ball.get_position() for ball in player.balls]
            for player in players.values()
        })

    def set_to_players(self, players: Dict[int, ClientPlayer]):
        if len(players) != len(self.player_id_2_ball_position):
            print("Received positions with wrong len:", len(players), len(self.player_id_2_ball_position))
            return
        for player in players.values():
            ball_positions_to_set = self.player_id_2_ball_position[player.player_id]
            assert len(ball_positions_to_set) == len(player.balls)
            for ball, ball_position in zip(player.balls, ball_positions_to_set):
                ball.setPos(ball_position.to_q_point_f())
