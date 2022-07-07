from typing import List
from balls_positions import BallPosition


class TargetsForBallsMessage:
    def __init__(self, player_id: int, indices: List[int], position: BallPosition):
        self.player_id = player_id
        self.indices = indices
        self.position = position
