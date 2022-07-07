from typing import Union, List
from PyQt6.QtCore import QObject, pyqtSignal, QByteArray
from balls_positions import BallsPositions
from jump_message import JumpMessage
from net_address import NetAddress
from targets_for_selected_balls import TargetsForBallsMessage
from udp_message_translator import UDPMessageTranslator


class UDPHandler(QObject):
    jump_signal = pyqtSignal(JumpMessage)
    set_target_signal = pyqtSignal(TargetsForBallsMessage)
    set_pos_signal = pyqtSignal(BallsPositions)

    def __init__(
            self,
            target_net_addresses: List[NetAddress],
            listening_net_addresses: List[NetAddress],
    ):
        super().__init__()
        self._target_sockets = [
            target_net_address.connect_upd_socket(self)
            for target_net_address in target_net_addresses
        ]
        self._listening_sockets = [
            listening_net_address.bind_upd_socket(self)
            for listening_net_address in listening_net_addresses
        ]
        for socket in self._listening_sockets:
            socket.readyRead.connect(self.receive_bytes)

    def receive_bytes(self):
        for socket in self._listening_sockets:
            while socket.hasPendingDatagrams():
                datagram = QByteArray()
                datagram.resize(socket.pendingDatagramSize())
                message_bytes, _, _ = socket.readDatagram(datagram.size())
                obj = UDPMessageTranslator.from_bytes(message_bytes)
                if isinstance(obj, BallsPositions):
                    self.set_pos_signal.emit(obj)
                elif isinstance(obj, TargetsForBallsMessage):
                    self.set_target_signal.emit(obj)
                else:
                    self.jump_signal.emit(obj)

    def send_obj(self, obj=Union[BallsPositions, JumpMessage, TargetsForBallsMessage]):
        obj_in_bytes = UDPMessageTranslator.to_bytes(obj)
        for socket in self._target_sockets:
            socket.write(obj_in_bytes)
