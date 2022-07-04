import sys

from PyQt6.QtCore import QRectF, QPointF, QSizeF, Qt
from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtWidgets import QApplication, QAbstractScrollArea
from ball_widget import BallWidget
from client_ball import ClientBall
from client_scene import ClientScene
from udp_handler import UDPHandler


def run_client():
    app = QApplication(sys.argv)
    client_balls = [
            ClientBall(
                x=200,
                y=350,
                default_color="red",
                hover_color="darkred",
                radius=100,
            ),
            ClientBall(
                x=400,
                y=350,
                default_color="blue",
                hover_color="darkblue",
                radius=75,
            ),
            ClientBall(
                x=550,
                y=350,
                default_color="green",
                hover_color="darkgreen",
                radius=50,
            ),
            ClientBall(
                x=650,
                y=350,
                default_color="orange",
                hover_color="darkorange",
                radius=25,
            ),
        ]
    client_scene = ClientScene(client_balls)
    client_udp_handler = UDPHandler(
        target_port=8888,
        listening_port=7777,
        target_host=QHostAddress.SpecialAddress.LocalHostIPv6,
        listening_host=QHostAddress.SpecialAddress.LocalHostIPv6,
    )
    client_scene.jump_signal.connect(client_udp_handler.send_obj)
    client_scene.set_target_signal.connect(client_udp_handler.send_obj)
    client_udp_handler.set_pos_signal.connect(client_scene.get_balls_position)
    widget = BallWidget(client_scene=client_scene)
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
    run_client()
