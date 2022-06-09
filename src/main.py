import sys
from PyQt6.QtWidgets import QApplication
from selecting_rect import SelectingRect
from ball import Ball
from ball_widget import BallWidget


def main():
    app = QApplication(sys.argv)
    widget = BallWidget(
        selecting_rect=SelectingRect(),
        frame_per_second=60,
        balls=[
            Ball(x=100, y=250, default_color="red", hover_color="darkred", radius=70, speed=1, jump_len=20),
            Ball(x=225, y=250, default_color="blue", hover_color="darkblue", radius=50, speed=2, jump_len=40),
            Ball(x=325, y=250, default_color="green", hover_color="darkgreen", radius=40, speed=3, jump_len=80),
            Ball(x=400, y=250, default_color="orange", hover_color="darkorange", radius=20, speed=4, jump_len=160),
        ]
    )
    widget.setWindowTitle("BallGame")
    widget.size()
    widget.setMouseTracking(True)
    widget.showFullScreen()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
