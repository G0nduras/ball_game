from typing import List
from server_ball import ServerBall


class ServerPlayer:
    def __init__(
            self,
            players_id: int,
            balls: List[ServerBall]
    ):
        self.players_id = players_id
        self.balls: List[ServerBall] = balls
