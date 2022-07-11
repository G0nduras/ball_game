import sys
from PyQt6.QtCore import QRectF, QPointF, QSizeF, Qt
from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtWidgets import QApplication, QAbstractScrollArea
from ball_widget import BallWidget
from client_ball import ClientBall
from client_scene import ClientScene
from network.net_address import NetAddress
from src.network.udp_handler import UDPHandler
from client_player import ClientPlayer


PLAYERS_COUNT = 2
SERVER_IP = "127.0.0.1"
PLAYER_ID = 0


def run_client():
    app = QApplication(sys.argv)
    players = [
        ClientPlayer(players_id=0, balls=[ClientBall(
            x=400,
            y=350,
            default_color="blue",
            radius=75,
        )]),
        ClientPlayer(players_id=1, balls=[ClientBall(
            x=400 * 2,
            y=350,
            default_color="red",
            radius=75,
        )]),
    ]
    client_scene = ClientScene(client_players=players, player_id=PLAYER_ID)
    if PLAYER_ID == 0:
        client_udp_handler = UDPHandler(
            listening_net_addresses=[
                NetAddress(host=QHostAddress.SpecialAddress.LocalHost, port=12342),
            ],
            target_net_addresses=[
                NetAddress(host=QHostAddress.SpecialAddress.LocalHost, port=12340),
            ],
        )
    else:
        client_udp_handler = UDPHandler(
            listening_net_addresses=[
                NetAddress(host=QHostAddress.SpecialAddress.LocalHost, port=12343),
            ],
            target_net_addresses=[
                NetAddress(host=QHostAddress(SERVER_IP), port=12341),
            ],
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
