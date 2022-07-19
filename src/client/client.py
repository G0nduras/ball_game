from typing import Optional

from PyQt6.QtCore import QRectF, QSizeF, QPointF, Qt, pyqtSlot, QObject
from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtWidgets import QAbstractScrollArea

from omegaconf import DictConfig

from src.client.ball_widget import BallWidget
from src.client.client_ball import ClientBall
from src.client.client_player import ClientPlayer
from src.client.client_scene import ClientScene
from src.network.net_address import NetAddress
from src.network.new_client_info_message import NewClientInfoMessage
from src.network.new_client_message import NewClientMessage
from src.network.new_player_message import NewPlayerMessage
from src.network.tcp_handler import TCPHandler
from src.network.udp_handler import UDPHandler


class Client(QObject):
    def __init__(
            self,
            client_conf: DictConfig,
    ):
        super().__init__()
        self._client_conf = client_conf
        self._client_scene: Optional[ClientScene] = None

        self._udp_handler: UDPHandler = UDPHandler(listening_port=client_conf.client_udp_port)
        self._tcp_handler: TCPHandler = TCPHandler(listening_port=client_conf.client_tcp_port)
        self._udp_handler.add_target_address(NetAddress(
            host=QHostAddress(client_conf.server_host),
            port=client_conf.server_udp_port,
        ))
        self._tcp_handler.add_target_address(NetAddress(
            host=QHostAddress(client_conf.server_host),
            port=client_conf.server_tcp_port,
        ))
        self._tcp_handler.new_client_info_signal.connect(self.process_new_client_info_message)
        self._tcp_handler.new_player_signal.connect(self.process_new_player)

        self._tcp_handler.send_obj_to_last(NewClientMessage(
            spawn_x=self._client_conf.ball_spawn_x,
            spawn_y=self._client_conf.ball_spawn_y,
            radius=self._client_conf.ball_radius,
            default_color=self._client_conf.ball_color,
            tcp_host=self._client_conf.client_host,
            tcp_port=self._client_conf.client_tcp_port,
            udp_host=self._client_conf.client_host,
            udp_port=self._client_conf.client_udp_port,
        ))
        self._widget = BallWidget()
        self._widget.setWindowTitle("BallGame")
        self._widget.setMouseTracking(True)
        self._widget.showFullScreen()
        widget_size = self._widget.size()
        self._widget.setSceneRect(QRectF(QPointF(0, 0), QSizeF(widget_size)))
        self._widget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        self._widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    @pyqtSlot(NewPlayerMessage)
    def process_new_player(self, new_player: NewPlayerMessage):
        self._client_scene.add_player(ClientPlayer(
            players_id=new_player.player_id,
            balls=[
                ClientBall(
                    x=new_player.spawn_x,
                    y=new_player.spawn_y,
                    default_color=new_player.default_color,
                    radius=new_player.radius
                )
            ]
        ))

    @pyqtSlot(NewClientInfoMessage)
    def process_new_client_info_message(self, new_client_info_message: NewClientInfoMessage):
        self._client_scene = ClientScene(player_id=new_client_info_message.player_id)

        self._client_scene.add_player(player=ClientPlayer(
            players_id=new_client_info_message.player_id,
            balls=[ClientBall(
                x=self._client_conf.ball_spawn_x,
                y=self._client_conf.ball_spawn_y,
                radius=self._client_conf.ball_radius,
                default_color=self._client_conf.ball_color,
            )],
        ))

        for player in new_client_info_message.other_players:
            client_player = ClientPlayer(players_id=new_client_info_message.player_id, balls=[ClientBall(
                x=player.spawn_x,
                y=player.spawn_y,
                radius=player.radius,
                default_color=player.default_color,
            )])
            self._client_scene.add_player(client_player)

        self._widget.set_scene(client_scene=self._client_scene)

        self._client_scene.jump_signal.connect(self._udp_handler.send_obj)
        self._client_scene.set_target_signal.connect(self._udp_handler.send_obj)
        self._udp_handler.set_pos_signal.connect(self._client_scene.get_balls_position)
