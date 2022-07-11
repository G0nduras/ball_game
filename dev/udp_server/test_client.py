import sys

from PyQt6.QtCore import QObject, QByteArray
from PyQt6.QtNetwork import QHostAddress, QUdpSocket
from PyQt6.QtWidgets import QApplication


class UDPClient(QObject):
    def __init__(self, port=8787):
        super().__init__()
        self._socket = QUdpSocket(self)
        self._socket.bind(QHostAddress.SpecialAddress.LocalHostIPv6, port)
        self._socket.readyRead.connect(self.writing)

    def writing(self):
        print("Recived data")
        while self._socket.hasPendingDatagrams():
            datagram = QByteArray()
            datagram.resize(self._socket.pendingDatagramSize())
            data, _, _ = self._socket.readDatagram(datagram.size())
            print(data.decode("utf-8"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = UDPClient()
    sys.exit(app.exec())
