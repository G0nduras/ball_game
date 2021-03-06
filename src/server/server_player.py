from typing import List

from src.network.new_player_message import NewPlayerMessage
from server_ball import ServerBall


class ServerPlayer:
    def __init__(
            self,
            player_id: int,
            balls: List[ServerBall]
    ):
        self.player_id = player_id
        self.balls: List[ServerBall] = balls

    def create_new_player_message(self) -> NewPlayerMessage:
        assert len(self.balls) == 1
        ball: ServerBall = self.balls[0]
        return NewPlayerMessage(
            player_id=self.player_id,
            spawn_x=round(ball.pos().x()),
            spawn_y=round(ball.pos().y()),
            radius=ball._radius,
            default_color=ball._ball_color,
        )
