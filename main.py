import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, e):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("red"), Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(200, 200, 100, 100)


def main():
    app = QApplication(sys.argv)
    widget = CircleWidget()
    widget.setWindowTitle("BallGame")
    widget.setFixedSize(QSize(500, 500))
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
