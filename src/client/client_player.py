from typing import List
from src.client.client_ball import ClientBall


class ClientPlayer:
    def __init__(
            self,
            player_id: int,
            balls: List[ClientBall]
    ):
        self.player_id = player_id
        self.balls: List[ClientBall] = balls
