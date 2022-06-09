import sys

from math import sin, cos, pi
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem, QApplication


class TestWidget(QGraphicsView):
    pass


class TestBall:
    def __init__(self, ball_graphics_item):
        self._t = 0
        self._ball_graphics_item = ball_graphics_item

    def step(self):
        self._t += 1
        t0 = 500
        radius = 100
        self._ball_graphics_item.setX((radius * sin((2 * pi * self._t) / t0)))
        self._ball_graphics_item.setY((radius * cos((2 * pi * self._t) / t0)))


def main():
    app = QApplication(sys.argv)
    widget = TestWidget()
    scene = QGraphicsScene()
    brush = QBrush(QColor("red"), style=Qt.BrushStyle.SolidPattern)
    ball = TestBall(QGraphicsEllipseItem(10, 10, 100, 100))
    ball._ball_graphics_item.setBrush(brush)
    scene.addItem(ball._ball_graphics_item)
    timer = QTimer()
    def on_timer_tick():
        ball.step()
        #scene.update()

    timer.timeout.connect(on_timer_tick)
    timer.start(round(1000 / 120))

    widget.setScene(scene)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

