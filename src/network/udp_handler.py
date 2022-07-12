from typing import Union, List
from PyQt6.QtCore import QObject, pyqtSignal, QByteArray
from src.network.balls_positions import BallsPositionsMessage
from src.network.jump_message import JumpMessage
from src.network.net_address import NetAddress
from src.network.targets_for_balls_message import TargetsForBallsMessage
from src.network.udp_message_translator import UDPMessageTranslator


class UDPHandler(QObject):
    jump_signal = pyqtSignal(JumpMessage)
    set_target_signal = pyqtSignal(TargetsForBallsMessage)
    set_pos_signal = pyqtSignal(BallsPositionsMessage)

    def __init__(
            self,
            target_net_addresses: List[NetAddress],
            listening_net_address: NetAddress,
    ):
        super().__init__()
        self._target_sockets = [
            target_net_address.connect_upd_socket(self)
            for target_net_address in target_net_addresses
        ]
        self._listening_socket = listening_net_address.bind_upd_socket(self)
        self._listening_socket.readyRead.connect(self.receive_bytes)

    def receive_bytes(self):
        while self._listening_socket.hasPendingDatagrams():
            datagram = QByteArray()
            datagram.resize(self._listening_socket.pendingDatagramSize())
            message_bytes, _, _ = self._listening_socket.readDatagram(datagram.size())
            obj = UDPMessageTranslator.from_bytes(message_bytes)
            if isinstance(obj, BallsPositionsMessage):
                self.set_pos_signal.emit(obj)
            elif isinstance(obj, TargetsForBallsMessage):
                self.set_target_signal.emit(obj)
            else:
                self.jump_signal.emit(obj)

    def send_obj(self, obj=Union[BallsPositionsMessage, JumpMessage, TargetsForBallsMessage]):
        obj_in_bytes = UDPMessageTranslator.to_bytes(obj)
        for socket in self._target_sockets:
            socket.write(obj_in_bytes)
