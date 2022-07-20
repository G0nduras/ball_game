from typing import Union, List
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtNetwork import QTcpSocket, QAbstractSocket, QHostAddress, QTcpServer
from src.network.new_client_info_message import NewClientInfoMessage
from src.network.udp_message_translator import UDPMessageTranslator
from src.network.net_address import NetAddress
from src.network.new_player_message import NewPlayerMessage
from src.network.new_client_message import NewClientMessage


class TCPHandler(QTcpServer):
    new_player_signal = pyqtSignal(NewPlayerMessage)
    new_client_signal = pyqtSignal(NewClientMessage)
    new_client_info_signal = pyqtSignal(NewClientInfoMessage)

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
        print("new_connection")
        client_socket: QTcpSocket = self.nextPendingConnection()
        client_socket.readyRead.connect(self.receive_bytes)
        client_socket.stateChanged.connect(self.on_socket_change)
        self._sockets.append(client_socket)
        print("len, sockets", len(self._sockets))

    def receive_bytes(self):
        print("receive_bytes")
        sender = self.sender()
        data = sender.readAll()
        obj = UDPMessageTranslator.from_bytes(data)
        print("type obj:", type(obj))
        if isinstance(obj, NewPlayerMessage):
            self.new_player_signal.emit(obj)
        elif isinstance(obj, NewClientMessage):
            self.new_client_signal.emit(obj)
        else:
            assert isinstance(obj, NewClientInfoMessage)
            self.new_client_info_signal.emit(obj)

    def on_socket_change(self, socket_state):
        print("on_socket_change, type socket_state:", type(socket_state))
        if socket_state == QAbstractSocket.SocketState.UnconnectedState:
            sender = self.sender()
            self._sockets.remove(sender)

    def add_target_address(self, target_net_address: NetAddress):
        print("add_target_address host:", target_net_address._host, "port:", target_net_address._port)
        self._target_net_addresses.append(target_net_address)
        print("len target_net_address", len(self._target_net_addresses))

    def send_obj_to_all(self, obj: Union[NewPlayerMessage, NewClientMessage]):
        print("send_obj_to_all: obj type:", type(obj))
        for target_net_address in self._target_net_addresses:
            obj_in_bytes = UDPMessageTranslator.to_bytes(obj)
            socket = target_net_address.connect_tcp_socket(self)
            socket.write(obj_in_bytes)

    def send_obj_to_last(self, obj: Union[NewPlayerMessage, NewClientMessage, NewClientInfoMessage]):
        last_address = self._target_net_addresses[-1]
        print("send_obj_to_last: obj type:", type(obj), "host:", str(last_address._host), "port:", last_address._port)
        obj_in_bytes = UDPMessageTranslator.to_bytes(obj)
        socket = last_address.connect_tcp_socket(self)
        socket.write(obj_in_bytes)
