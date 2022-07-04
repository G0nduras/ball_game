from typing import List
from balls_positions import BallPosition


class TargetsForSelectedBalls:
    def __init__(self, indices: List[int], position: BallPosition):
        self._indices = indices
        self._position = position
