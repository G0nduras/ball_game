import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._x = 200
        self._y = 200

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("red"), Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(self._x, self._y, 100, 100)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self._x -= 10
        elif event.key() == Qt.Key.Key_Right:
            self._x += 10
        elif event.key() == Qt.Key.Key_Up:
            self._y -= 10
        elif event.key() == Qt.Key.Key_Down:
            self._y += 10
        if self._x > 400:
            self._x = 400
        elif self._x < 0:
            self._x = 0
        elif self._y > 400:
            self._y = 400
        elif self._y < 0:
            self._y = 0
        self.update()


def main():
    app = QApplication(sys.argv)
    widget = CircleWidget()
    widget.setWindowTitle("BallGame")
    widget.setFixedSize(QSize(500, 500))
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
