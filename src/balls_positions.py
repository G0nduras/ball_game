from typing import List
from PyQt6.QtCore import QPointF


class BallPosition:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def to_q_point_f(self):
        return QPointF(self.x, self.y)


class BallsPositions:
    def __init__(self, balls_positions: List[BallPosition]):
        self.balls_positions: List[BallPosition] = balls_positions

    @staticmethod
    def from_balls(balls: List['Ball']):
        #return BallsPositions(balls_positions=list(map(Ball.get_position, balls)))
        return BallsPositions(balls_positions=[
            ball.get_position()
            for ball in balls
        ])

    def set_to_balls(self, balls: List['Ball']):
        assert len(balls) == len(self.balls_positions), (len(balls), len(self.balls_positions))
        for ball, ball_position in zip(balls, self.balls_positions):
            ball.setPos(QPointF(ball_position.x, ball_position.y))
