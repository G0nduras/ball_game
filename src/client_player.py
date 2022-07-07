from typing import List
from client_ball import ClientBall


class ClientPlayer:
    def __init__(
            self,
            players_id: int,
            balls: List[ClientBall]
    ):
        self.players_id = players_id
        self.balls: List[ClientBall] = balls
