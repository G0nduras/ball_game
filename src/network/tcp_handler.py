from typing import Union, List, Dict
import random
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtNetwork import QTcpSocket, QAbstractSocket, QHostAddress, QTcpServer
from src.network.client_dicsonnected_message import ClientDisconnectedMessage
from src.network.new_client_info_message import NewClientInfoMessage
from src.network.udp_message_translator import MessageTranslator
from src.network.net_address import NetAddress
from src.network.new_player_message import NewPlayerMessage
from src.network.new_client_message import NewClientMessage


class TCPHandler(QTcpServer):
    new_player_signal = pyqtSignal(NewPlayerMessage)
    new_client_signal = pyqtSignal(NewClientMessage)
    new_client_info_signal = pyqtSignal(NewClientInfoMessage)
    client_disconnected_signal = pyqtSignal(ClientDisconnectedMessage)

    def __init__(
            self,
            listening_port: int,
    ):
        super().__init__()
        self._target_net_addresses: Dict[int, NetAddress] = {}

        self.listen(QHostAddress.SpecialAddress.Any, listening_port)
        self.newConnection.connect(self.new_connection)
        self._sockets: List[QTcpSocket] = []

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
        obj = MessageTranslator.from_bytes(data)
        print("type obj:", type(obj))
        if isinstance(obj, NewPlayerMessage):
            self.new_player_signal.emit(obj)
        elif isinstance(obj, NewClientMessage):
            self.new_client_signal.emit(obj)
        elif isinstance(obj, NewClientInfoMessage):
            self.new_client_info_signal.emit(obj)
        else:
            assert isinstance(obj, ClientDisconnectedMessage), type(obj)
            self.client_disconnected_signal.emit(obj)

    def on_socket_change(self, socket_state):
        print("on_socket_change sockets number in the beginning", len(self._sockets))
        if socket_state == QAbstractSocket.SocketState.UnconnectedState:
            sender = self.sender()
            self._sockets.remove(sender)
        print("on_socket_change sockets number in the end:", len(self._sockets))

    def add_target_address_with_random_key(self, target_net_address: NetAddress):
        key = random.randint(0, 1e10)
        while key in self._target_net_addresses:
            key = random.randint(0, 1e10)
        self.add_target_address(key=key, target_net_address=target_net_address)

    def add_target_address(self, key: int, target_net_address: NetAddress):
        print("add_target_address host:", target_net_address._host, "port:", target_net_address._port)
        self._target_net_addresses[key] = target_net_address
        print("len target_net_address", len(self._target_net_addresses))

    def remove_target_address(self, key: int):
        self._target_net_addresses.pop(key)

    def send_obj_to_all(self, obj: Union[NewPlayerMessage, NewClientMessage, ClientDisconnectedMessage]):
        print("send_obj_to_all: obj type:", type(obj), "targets len:", len(self._target_net_addresses))
        for target_net_address in self._target_net_addresses.values():
            obj_in_bytes = MessageTranslator.to_bytes(obj)
            socket = target_net_address.connect_tcp_socket(self)
            socket.write(obj_in_bytes)
        print("send_obj_to_all finished")

    def send_obj_to_last(self, obj: Union[NewPlayerMessage, NewClientMessage, NewClientInfoMessage]):
        last_address = list(self._target_net_addresses.values())[-1]
        print("send_obj_to_last: obj type:", type(obj), "host:", str(last_address._host), "port:", last_address._port)
        obj_bytes = MessageTranslator.to_bytes(obj)
        socket = last_address.connect_tcp_socket(self)
        socket.write(obj_bytes)
        socket.waitForBytesWritten()
        socket.close()
        print("send_obj_to_last finished")
