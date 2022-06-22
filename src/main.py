import sys

from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt6.QtWidgets import QApplication, QAbstractScrollArea
from selecting_rect import SelectingRect
from ball import Ball
from ball_widget import BallWidget


def main():
    app = QApplication(sys.argv)
    impulse_module = 50000000
    trust_force_module = 100000
    resistance_alpha = 50
    density = 1
    widget = BallWidget(
        selecting_rect=SelectingRect(),
        frame_per_second=60,
        balls=[
            Ball(
                x=200,
                y=350,
                default_color="red",
                hover_color="darkred",
                radius=100,
                density=density,
                resistance_alpha=resistance_alpha,
                trust_force_module=trust_force_module,
                jump_impulse_module=impulse_module,
            ),
            Ball(
                x=400,
                y=350,
                default_color="blue",
                hover_color="darkblue",
                radius=75,
                density=density,
                resistance_alpha=resistance_alpha,
                trust_force_module=trust_force_module,
                jump_impulse_module=impulse_module,
            ),
            Ball(
                x=550,
                y=350,
                default_color="green",
                hover_color="darkgreen",
                radius=50,
                density=density,
                resistance_alpha=resistance_alpha,
                trust_force_module=trust_force_module,
                jump_impulse_module=impulse_module,
            ),
            Ball(
                x=650,
                y=350,
                default_color="orange",
                hover_color="darkorange",
                radius=25,
                density=density,
                resistance_alpha=resistance_alpha,
                trust_force_module=trust_force_module,
                jump_impulse_module=impulse_module,
            ),
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
