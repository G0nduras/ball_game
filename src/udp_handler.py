from typing import  Union, Tuple, List
from PyQt6.QtCore import QObject, pyqtSignal, QByteArray
from PyQt6.QtNetwork import QUdpSocket, QHostAddress
from balls_positions import BallsPositions, BallPosition
from udp_message_translator import UDPMessageTranslator


Target = Tuple[List[int], BallPosition]
Jump = List[int]


class UDPHandler(QObject):
    jump_signal = pyqtSignal(list)
    set_target_signal = pyqtSignal(list, BallPosition)
    set_pos_signal = pyqtSignal(BallsPositions)

    def __init__(
            self,
            target_host: QHostAddress,
            target_port: int,
            listening_host: QHostAddress,
            listening_port: int,
    ):
        super().__init__()
        self._target_socket = QUdpSocket(self)
        self._target_socket.connectToHost(target_host, target_port)
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
            elif isinstance(obj, tuple):
                indices, position = obj
                assert isinstance(indices, list), type(indices)
                assert isinstance(position, BallPosition), type(position)
                self.set_target_signal.emit(indices, position)
            else:
                self.jump_signal.emit(obj)

    def send_obj(self, obj=Union[BallsPositions, Jump, Target]):
        obj_in_bytes = UDPMessageTranslator.to_bytes(obj)
        self._target_socket.write(obj_in_bytes)
