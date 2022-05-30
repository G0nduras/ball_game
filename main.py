import sys
from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class CircleWidget(QWidget):
    def __init__(
            self,
            width: float,
            height: float,
            circle_radius: float,
            circle_color: str,
            step: float,
    ):
        super().__init__()
        self._width: float = width
        self._height: float = height
        self._x: float = height / 2 - circle_radius
        self._y: float = width / 2 - circle_radius
        self._circle_radius: float = circle_radius
        self._circle_color: str = circle_color
        self._step: float = step
        self._x_mouse_position: Optional[float] = None
        self._y_mouse_position: Optional[float] = None

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(self._circle_color), Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(
            round(self._x),
            round(self._y),
            round(self._circle_radius * 2),
            round(self._circle_radius * 2),
        )

    def _compute_next_x_y(self, event):
        x = self._x
        y = self._y
        if event.key() == Qt.Key.Key_Left:
            x -= self._step
        elif event.key() == Qt.Key.Key_Right:
            x += self._step
        elif event.key() == Qt.Key.Key_Up:
            y -= self._step
        elif event.key() == Qt.Key.Key_Down:
            y += self._step
        return x, y

    def _is_out_of_range(self, x: float, y: float):
        max_x = self._height - 2 * self._circle_radius
        max_y = self._width - 2 * self._circle_radius
        return (x < 0) or (y < 0) or (x > max_x) or (y > max_y)

    def keyPressEvent(self, event):
        new_x, new_y = self._compute_next_x_y(event=event)
        if not self._is_out_of_range(x=new_x, y=new_y):
            self._x = new_x
            self._y = new_y
            self.update()

    def mouseMoveEvent(self, event):
        x_mouse_position = event.pos().x()
        y_mouse_position = event.pos().y()

    def mousePressEvent(self, event):
        self._x = event.pos().x() - self._circle_radius
        self._y = event.pos().y() - self._circle_radius
        self.update()


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500


def main():
    app = QApplication(sys.argv)
    widget = CircleWidget(
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        circle_radius=50,
        circle_color="red",
        step=10,
    )
    widget.setWindowTitle("BallGame")
    widget.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    widget.setMouseTracking(True)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
