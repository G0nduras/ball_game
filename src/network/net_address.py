from PyQt6.QtCore import QObject
from PyQt6.QtNetwork import QHostAddress, QUdpSocket


class NetAddress:
    def __init__(self, host: QHostAddress, port: int):
        super().__init__()
        self._host = host
        self._port = port

    def connect_upd_socket(self, q_object) -> QUdpSocket:
        socket = QUdpSocket(q_object)
        socket.connectToHost(self._host, self._port)
        return socket

    def bind_upd_socket(self, q_object) -> QUdpSocket:
        socket = QUdpSocket(q_object)
        socket.bind(self._host, self._port)
        return socket
