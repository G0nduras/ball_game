from typing import Optional, List

from PyQt6.QtCore import QRectF, QSizeF, QPointF, Qt
from PyQt6.QtWidgets import QAbstractScrollArea
from client.ball_widget import BallWidget
from client.client_ball import ClientBall
from client.client_player import ClientPlayer
from client.client_scene import ClientScene
from network.new_client_info_message import NewClientInfoMessage
from network.new_client_message import NewClientMessage
from network.tcp_handler import TCPHandler
from network.udp_handler import UDPHandler
from omegaconf import DictConfig


class Client:
    def __init__(
            self,
            client_conf: DictConfig,
    ):
        self._client_conf = client_conf
        self._client_scene: Optional[ClientScene] = None

        self._udp_handler: UDPHandler = UDPHandler(listening_port=client_conf.udp_port)
        self._tcp_handler: TCPHandler = TCPHandler(listening_port=client_conf.tcp_port)

        self._tcp_handler.send_obj_to_last(NewClientMessage(
            spawn_x=self._client_conf.ball_spawn_x,
            spawn_y=self._client_conf.ball_spawn_y,
            radius=self._client_conf.ball_radius,
            default_color=self._client_conf.ball_color,
            tcp_host=self._client_conf.server_host,
            tcp_port=self._client_conf.server_tcp_port,
            udp_host=self._client_conf.server_host,
            udp_port=self._client_conf.server_udp_port,
        ))

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

        widget = BallWidget(client_scene=self._client_scene)
        widget.setWindowTitle("BallGame")
        widget.setMouseTracking(True)
        widget.showFullScreen()
        widget_size = widget.size()
        widget.setSceneRect(QRectF(QPointF(0, 0), QSizeF(widget_size)))
        widget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
        widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._client_scene.jump_signal.connect(self._udp_handler.send_obj)
        self._client_scene.set_target_signal.connect(self._udp_handler.send_obj)
        self._udp_handler.set_pos_signal.connect(self._client_scene.get_balls_position)
