import sys

from PyQt6.QtCore import QObject, QByteArray
from PyQt6.QtNetwork import QHostAddress, QTcpSocket
from PyQt6.QtWidgets import QApplication


class TCPClient(QObject):
    def __init__(self, port=12345):
        super().__init__()
        self._socket = QTcpSocket(self)
        self._socket.connectToHost(QHostAddress.SpecialAddress.LocalHost, port)

    def write(self, message):
        self._socket.write(message.encode("utf-8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = TCPClient()
    client.write("Hello, world")
    sys.exit(app.exec())
