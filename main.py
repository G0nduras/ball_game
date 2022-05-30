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
            hover_circle_color: str,
            step: float,
    ):
        super().__init__()
        self._width: float = width
        self._height: float = height
        self._x: float = height / 2 - circle_radius
        self._y: float = width / 2 - circle_radius
        self._circle_radius: float = circle_radius
        self._circle_color: str = circle_color
        self._hover_circle_color = hover_circle_color
        self._step: float = step
        self._mouse_position_x: Optional[float] = None
        self._mouse_position_y: Optional[float] = None

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor(self._get_circle_color()), Qt.BrushStyle.SolidPattern))
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

    def _get_circle_center(self):
        return self._x + self._circle_radius, self._y + self._circle_radius

    def _get_circle_color(self):
        if self._mouse_position_x is None:
            return self._circle_color

        circle_center_x, circle_center_y = self._get_circle_center()
        square_distance = (circle_center_x - self._mouse_position_x) ** 2 + (circle_center_y - self._mouse_position_y) ** 2
        if square_distance < self._circle_radius ** 2:
            return self._hover_circle_color
        else:
            return self._circle_color

    def mouseMoveEvent(self, event):
        color_before = self._get_circle_color()
        self._mouse_position_x = event.pos().x()
        self._mouse_position_y = event.pos().y()
        color_after = self._get_circle_color()
        if color_before != color_after:
            self.update()

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
        hover_circle_color="green",
        step=10,
    )
    widget.setWindowTitle("BallGame")
    widget.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    widget.setMouseTracking(True)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
