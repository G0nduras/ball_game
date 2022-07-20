from typing import List

from omegaconf import DictConfig

from PyQt6.QtCore import pyqtSlot, QObject
from PyQt6.QtNetwork import QHostAddress
from src.network.net_address import NetAddress
from src.network.new_client_info_message import NewClientInfoMessage
from src.network.tcp_handler import TCPHandler
from src.network.udp_handler import UDPHandler
from src.network.new_client_message import NewClientMessage
from src.server.server_ball import ServerBall
from src.server.server_player import ServerPlayer
from src.server.server_scene import ServerScene


class Server(QObject):
    def __init__(
            self,
            server_conf: DictConfig,
    ):
        super().__init__()
        self._server_conf = server_conf

        self._server_scene: ServerScene = ServerScene(frame_per_second=server_conf.frame_per_second)
        self._udp_handler: UDPHandler = UDPHandler(listening_port=server_conf.udp_port)
        self._tcp_handler: TCPHandler = TCPHandler(listening_port=server_conf.tcp_port)

        self._udp_handler.jump_signal.connect(self._server_scene.set_jump)
        self._udp_handler.set_target_signal.connect(self._server_scene.set_target_for_selected_balls)
        self._server_scene.set_pos_signal.connect(self._udp_handler.send_obj)
        self._tcp_handler.new_client_signal.connect(self.process_new_client)

    @pyqtSlot(NewClientMessage)
    def process_new_client(self, new_client_message: NewClientMessage):
        player_id = self._server_scene.get_new_player_id()
        self._tcp_handler.send_obj_to_all(new_client_message.to_new_player_message(player_id=player_id))
        self._udp_handler.add_target_address(target_net_address=NetAddress(
            host=QHostAddress(new_client_message.udp_host),
            port=new_client_message.udp_port,
        ))
        self._tcp_handler.add_target_address(target_net_address=NetAddress(
            host=QHostAddress(new_client_message.tcp_host),
            port=new_client_message.tcp_port,
        ))
        other_players = [
            player.create_new_player_message()
            for player in self._server_scene._server_players
        ]
        self._tcp_handler.send_obj_to_last(NewClientInfoMessage(
            player_id=player_id,
            other_players=other_players,
        ))
        self._server_scene.add_player(player=ServerPlayer(players_id=player_id, balls=[ServerBall(
            x=new_client_message.spawn_x,
            y=new_client_message.spawn_y,
            radius=new_client_message.radius,
            density=self._server_conf.density,
            resistance_alpha=self._server_conf.resistance_alpha,
            thrust_force_module=self._server_conf.trust_force_module,
            jump_impulse_module=self._server_conf.impulse_module,
        )]))