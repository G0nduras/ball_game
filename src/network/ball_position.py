from PyQt6.QtCore import QPointF


class BallPosition:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def to_q_point_f(self):
        return QPointF(self.x, self.y)
