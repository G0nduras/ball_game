from typing import List, Tuple

from PyQt6.QtCore import QPointF
from ball import Ball


class BallsPositions:
    def __init__(self, balls_positions: List[Tuple[float, float]]):
        self.balls_positions = balls_positions

    @staticmethod
    def from_balls(balls: List[Ball]):
        #return BallsPositions(balls_positions=list(map(Ball.get_position, balls)))
        return BallsPositions(balls_positions=[
            ball.get_position()
            for ball in balls
        ])

    def set_to_balls(self, balls: List[Ball]):
        assert len(balls) == len(self.balls_positions), (len(balls), len(self.balls_positions))
        for ball, (x, y) in zip(balls, self.balls_positions):
            ball.setPos(QPointF(x, y))
