from typing import List

from src.network.new_player_message import NewPlayerMessage
from server_ball import ServerBall


class ServerPlayer:
    def __init__(
            self,
            players_id: int,
            balls: List[ServerBall]
    ):
        self.players_id = players_id
        self.balls: List[ServerBall] = balls

    @staticmethod
    def create_new_player_message(self) -> NewPlayerMessage:
        assert len(self.balls) == 1
        ball = self.balls[0]
        return NewPlayerMessage(
            player_id=self.players_id,
            spawn_x=ball.x,
            spawn_y=ball.y,
            default_color=ball.defauil_color,
            radius=ball.radius,
        )
