import sys
from PyQt6.QtWidgets import QApplication
from selecting_rect import SelectingRect
from ball import Ball
from ball_widget import BallWidget
from PyQt6.QtCore import QRect


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500


def main():
    app = QApplication(sys.argv)
    widget = BallWidget(
        selecting_rect=SelectingRect(),
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        step=10,
        frame_per_second=60,
        balls=[
            Ball(x=100, y=250, default_color="red", hover_color="darkred", radius=70, speed=1),
            Ball(x=225, y=250, default_color="blue", hover_color="darkblue", radius=50, speed=2),
            Ball(x=325, y=250, default_color="green", hover_color="darkgreen", radius=40, speed=3),
            Ball(x=400, y=250, default_color="orange", hover_color="darkorange", radius=20, speed=4),
        ]
    )
    widget.setWindowTitle("BallGame")
    widget.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    widget.setMouseTracking(True)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
