from typing import List
from PyQt6.QtCore import QPointF, QSizeF, QRectF, QPoint, Qt
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtWidgets import QGraphicsRectItem

from ball import Ball


class SelectingRect(QGraphicsRectItem):
    SMALL_RECT_AREA = 2 * 2

    def __init__(
            self,
    ):
        super().__init__()
        self.hide()

    def add_rect_to_scene(self, scene):
        self.setPen(QPen())
        self.setBrush(QBrush(QColor(0, 200, 0, 50), Qt.BrushStyle.SolidPattern))
        scene.addItem(self)

    def filter_selected_balls(self, balls: List[Ball]) -> List[Ball]:
        selected_balls = []
        for ball in balls:
            if ball.intersects_with_rect(rect=self.rect()):
                selected_balls.append(ball)
        return selected_balls

    def start_rect(self, mouse_click_pos: QPoint):
        self.setRect(QRectF(QPointF(mouse_click_pos), QSizeF(0, 0)))
        self.show()

    def expand_rect(self, mouse_position: QPoint):
        assert not self.is_none()
        rect = self.rect()
        delta_width: int = mouse_position.x() - rect.x() - rect.width()
        delta_height: int = mouse_position.y() - rect.y() - rect.height()
        self.setRect(QRectF(rect.topLeft(), QSizeF(rect.width() + delta_width, rect.height() + delta_height)))

    def clear_rect(self):
        self.hide()

    def is_none(self) -> bool:
        return not self.isVisible()

    def is_small(self) -> bool:
        rect = self.rect()
        return self.is_none() or (rect.width() * rect.height() < SelectingRect.SMALL_RECT_AREA)
