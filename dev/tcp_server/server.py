import sys

from PyQt6.QtCore import QTimer, QObject, QByteArray
from PyQt6.QtNetwork import QHostAddress, QTcpSocket, QTcpServer, QAbstractSocket, QLocalSocket
from PyQt6.QtWidgets import QApplication


class TCPServer(QTcpServer):
    def __init__(self, port=12345):
        super().__init__()
        self.listen(QHostAddress.SpecialAddress.Any, port)
        self.newConnection.connect(self.new_connection)
        self.sockets = []

    def new_connection(self):
        print("New connection!", len(self.sockets) + 1)
        client_socket: QTcpSocket = self.nextPendingConnection()
        client_socket.readyRead.connect(self.on_ready_read)
        client_socket.stateChanged.connect(self.on_socket_change)
        self.sockets.append(client_socket)

    def on_ready_read(self):
        print("New data!")
        sender = self.sender()
        data = sender.readAll()
        print(data, type(data))

    def on_socket_change(self, socket_state):
        print(1, socket_state)
        if socket_state == QAbstractSocket.SocketState.UnconnectedState:
            print(2)
            sender = self.sender()
            self.sockets.remove(sender)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tcp_server = TCPServer()
    sys.exit(app.exec())
