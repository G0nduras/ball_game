import sys

from PyQt6.QtCore import QTimer, QObject
from PyQt6.QtNetwork import QHostAddress, QUdpSocket
from PyQt6.QtWidgets import QApplication


class UDPServer(QObject):
    def __init__(self, port=8787):
        super().__init__()
        self._socket = QUdpSocket(self)
        self._socket.connectToHost(QHostAddress.SpecialAddress.LocalHostIPv6, port)

        self.timer = QTimer()
        self.timer.timeout.connect(self.write)
        self.timer.start(1000 * 3)
        self.counter = 0

    def write(self):
        self.counter += 1
        print(f"Sending... {self.counter}")
        self._socket.write(bytes("Hello", encoding="utf-8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = UDPServer()
    sys.exit(app.exec())
