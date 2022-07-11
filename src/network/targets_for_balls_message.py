from typing import List
from dataclasses import dataclass
from network.balls_positions import BallPosition


@dataclass
class TargetsForBallsMessage:
    player_id: int
    indices: List[int]
    position: BallPosition
