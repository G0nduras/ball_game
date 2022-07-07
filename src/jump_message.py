from typing import List


class JumpMessage:
    def __init__(
            self,
            player_indices: int,
            ball_indices: List[int],
    ):
        self.player_indices = player_indices
        self.ball_indices = ball_indices
