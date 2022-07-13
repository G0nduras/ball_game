from typing import Union, List
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtNetwork import QTcpSocket, QAbstractSocket, QHostAddress, QTcpServer
from src.network.udp_message_translator import UDPMessageTranslator
from src.network.net_address import NetAddress
from src.network.new_player_message import NewPlayerMessage
from src.network.new_client_message import NewClientMessage


class TCPHandler(QTcpServer):
    new_player_signal = pyqtSignal(NewPlayerMessage)
    new_client_signal = pyqtSignal(NewClientMessage)

    def __init__(
            self,
            listening_port: int,
    ):
        super().__init__()
        self._target_net_addresses: List[NetAddress] = []

        self.listen(QHostAddress.SpecialAddress.Any, listening_port)
        self.newConnection.connect(self.new_connection)
        self._sockets = []

    def new_connection(self):
        client_socket: QTcpSocket = self.nextPendingConnection()
        client_socket.readyRead.connect(self.receive_bytes)
        client_socket.stateChanged.connect(self.on_socket_change)
        self._sockets.append(client_socket)

    def receive_bytes(self):
        sender = self.sender()
        data = sender.readAll()
        obj = UDPMessageTranslator.from_bytes(data)
        self.new_player_signal.emit(obj)
        self.new_client_signal.emit(obj)

    def on_socket_change(self, socket_state):
        if socket_state == QAbstractSocket.SocketState.UnconnectedState:
            sender = self.sender()
            self._sockets.remove(sender)

    def add_target_address(self, target_net_address: NetAddress):
        self._target_net_addresses.append(target_net_address)

    def write_obj(self, obj: Union[NewPlayerMessage, NewClientMessage]):
        for target_net_address in self._target_net_addresses:
            obj_in_bytes = UDPMessageTranslator.to_bytes(obj)
            socket = target_net_address.connect_tcp_socket(self)
            socket.write(obj_in_bytes)
