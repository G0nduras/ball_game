from typing import Optional, List
from PyQt6.QtCore import QRect, QPointF, QSize, QPoint

from ball import Ball


class SelectingRect:
    def __init__(self):
        self._rect: Optional[QRect] = None

    def filter_selected_balls(self, balls: List[Ball]) -> List[Ball]:
        selected_balls = []
        for ball in balls:
            if ball.intersects_with_rect(rect=self._rect):
                selected_balls.append(ball)
        return selected_balls

    def start_rect(self, mouse_click_pos: QPointF):
        assert self._rect is None
        self._rect = QRect(mouse_click_pos.x(), mouse_click_pos.y(), 0, 0)

    def expand_rect(self, mouse_position: QPointF):
        assert self._rect is not None
        delta_width: int = mouse_position.x() - self._rect.x() - self._rect.width()
        delta_height: int = mouse_position.y() - self._rect.y() - self._rect.height()
        self._rect.adjust(0, 0, delta_width, delta_height)

    def clear_rect(self):
        self._rect = None

    def get_rect(self) -> QRect:
        assert self._rect is not None
        return self._rect

    def is_none(self) -> bool:
        return self._rect is None
