import sys

from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt6.QtWidgets import QApplication, QAbstractScrollArea
from selecting_rect import SelectingRect
from ball import Ball
from ball_widget import BallWidget


def main():
    app = QApplication(sys.argv)
    widget = BallWidget(
        selecting_rect=SelectingRect(),
        frame_per_second=60,
        balls=[
            Ball(x=200, y=350, default_color="red", hover_color="darkred", radius=100, power=100, jump_len=20, mass=1000, alpha=200),
            Ball(x=400, y=350, default_color="blue", hover_color="darkblue", radius=75, power=200, jump_len=40, mass=750, alpha=200),
            Ball(x=550, y=350, default_color="green", hover_color="darkgreen", radius=50, power=300, jump_len=80, mass=500, alpha=200),
            Ball(x=650, y=350, default_color="orange", hover_color="darkorange", radius=25, power=400, jump_len=160, mass=250, alpha=200),
        ],
    )
    widget.setWindowTitle("BallGame")
    widget.setMouseTracking(True)
    widget.showFullScreen()
    widget_size = widget.size()
    widget.setSceneRect(QRectF(QPointF(0, 0), QSizeF(widget_size)))
    widget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
    widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
