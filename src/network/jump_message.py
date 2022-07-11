from typing import List
from dataclasses import dataclass


@dataclass
class JumpMessage:
    player_indices: int
    ball_indices: List[int]