from typing import Union, List, Dict
import random
from PyQt6.QtCore import QObject, pyqtSignal, QByteArray
from PyQt6.QtNetwork import QHostAddress, QUdpSocket
from src.network.balls_positions import BallsPositionsMessage
from src.network.jump_message import JumpMessage
from src.network.net_address import NetAddress
from src.network.targets_for_balls_message import TargetsForBallsMessage
from src.network.udp_message_translator import MessageTranslator


class UDPHandler(QObject):
    jump_signal = pyqtSignal(JumpMessage)
    set_target_signal = pyqtSignal(TargetsForBallsMessage)
    set_pos_signal = pyqtSignal(BallsPositionsMessage)

    def __init__(
            self,
            listening_port: int,
    ):
        super().__init__()
        self._target_net_addresses: Dict[int, NetAddress] = {}
        self._target_sockets: Dict[int, QUdpSocket] = {}
        self._listening_net_address: NetAddress = NetAddress(
            host=QHostAddress("127.0.0.1"),
            port=listening_port,
        )
        self._listening_socket = self._listening_net_address.bind_upd_socket(self)
        self._listening_socket.readyRead.connect(self.receive_bytes)

    def add_target_address_with_random_key(self, target_net_address: NetAddress):
        key = random.randint(0, 1e10)
        while key in self._target_net_addresses:
            key = random.randint(0, 1e10)
        self.add_target_address(key=key, target_net_address=target_net_address)

    def add_target_address(self, key: int, target_net_address: NetAddress):
        print("UDPHandler: add_target_address, host:", target_net_address._host, "port:", target_net_address._port)
        self._target_net_addresses[key] = target_net_address
        new_target_socket = target_net_address.connect_upd_socket(self)
        self._target_sockets[key] = new_target_socket

    def remove_target_address(self, key: int):
        self._target_net_addresses.pop(key)
        self._target_sockets.pop(key)

    def receive_bytes(self):
        while self._listening_socket.hasPendingDatagrams():
            datagram = QByteArray()
            datagram.resize(self._listening_socket.pendingDatagramSize())
            message_bytes, _, _ = self._listening_socket.readDatagram(datagram.size())
            obj = MessageTranslator.from_bytes(message_bytes)
            if isinstance(obj, BallsPositionsMessage):
                self.set_pos_signal.emit(obj)
            elif isinstance(obj, TargetsForBallsMessage):
                self.set_target_signal.emit(obj)
            else:
                assert isinstance(obj, JumpMessage)
                self.jump_signal.emit(obj)

    def send_obj(self, obj=Union[BallsPositionsMessage, JumpMessage, TargetsForBallsMessage]):
        obj_in_bytes = MessageTranslator.to_bytes(obj)
        for socket in self._target_sockets.values():
            socket.write(obj_in_bytes)
