from typing import Union
from PyQt6.QtCore import QObject, pyqtSignal, QByteArray
from PyQt6.QtNetwork import QUdpSocket, QHostAddress
from balls_positions import BallsPositions
from jump_message import JumpMessage
from targets_for_selected_balls import TargetsForBallsMessage
from udp_message_translator import UDPMessageTranslator


class UDPHandler(QObject):
    jump_signal = pyqtSignal(JumpMessage)
    set_target_signal = pyqtSignal(TargetsForBallsMessage)
    set_pos_signal = pyqtSignal(BallsPositions)

    def __init__(
            self,
            target_host: QHostAddress.SpecialAddress,
            target_port: int,
            listening_host: QHostAddress.SpecialAddress,
            listening_port: int,
    ):
        super().__init__()
        self._target_socket = QUdpSocket(self)
        self._target_socket.connectToHost(target_host, target_port)
        self.counter = 0
        self._listening_socket = QUdpSocket(self)
        self._listening_socket.bind(listening_host, listening_port)
        self._listening_socket.readyRead.connect(self.receive_bytes)

    def receive_bytes(self):
        while self._listening_socket.hasPendingDatagrams():
            datagram = QByteArray()
            datagram.resize(self._listening_socket.pendingDatagramSize())
            message_bytes, _, _ = self._listening_socket.readDatagram(datagram.size())
            obj = UDPMessageTranslator.from_bytes(message_bytes)
            if isinstance(obj, BallsPositions):
                self.set_pos_signal.emit(obj)
            elif isinstance(obj, TargetsForBallsMessage):
                self.set_target_signal.emit(obj)
            else:
                self.jump_signal.emit(obj)

    def send_obj(self, obj=Union[BallsPositions, JumpMessage, TargetsForBallsMessage]):
        self.counter += 1
        obj_in_bytes = UDPMessageTranslator.to_bytes(obj)
        self._target_socket.write(obj_in_bytes)
