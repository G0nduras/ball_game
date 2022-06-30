from typing import List
from PyQt6.QtCore import QPointF, Qt, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QGraphicsScene
from client_ball import ClientBall
from selecting_rect import SelectingRect
from balls_positions import BallsPositions, BallPosition


class ClientScene(QGraphicsScene):
    jump_signal = pyqtSignal(list)
    set_target_signal = pyqtSignal(list, BallPosition)

    def __init__(
            self,
            balls: List[ClientBall],
    ):
        super().__init__()
        self._balls: List[ClientBall] = balls
        self._selected_balls: List[ClientBall] = []
        self._selecting_rect: SelectingRect = SelectingRect()

        for ball in balls:
            ball.add_ball_to_scene(self)

        self._selecting_rect.add_rect_to_scene(self)

    def key_press_event(self, event):
        if event.key() == Qt.Key.Key_Space:
            ball_indices = [
                ball_index
                for ball_index, ball in enumerate(self._balls)
                if ball in self._selected_balls
            ]
            self.jump_signal.emit(ball_indices)

    def mouse_move_event(self, event):
        if not self._selecting_rect.is_none():
            self._selecting_rect.expand_rect(event.pos())

    def mouse_release_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._selecting_rect.is_small():
                for ball in self._balls:
                    if ball.is_clicked(mouse_position=QPointF(event.pos())):
                        self._selected_balls = [ball]
                        break
                else:
                    self._selected_balls = []
            else:
                self._selected_balls = self._selecting_rect.filter_selected_balls(self._balls)
            for ball in self._balls:
                ball.set_draw_method(is_selected=ball in self._selected_balls)
            self._selecting_rect.clear_rect()

    def mouse_press_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self._selecting_rect.start_rect(event.pos())
        if event.buttons() == Qt.MouseButton.RightButton:
            if self._selected_balls is not None:
                ball_indices = [
                    ball_index
                    for ball_index, ball in enumerate(self._balls)
                    if ball in self._selected_balls
                ]
                self.set_target_signal.emit(ball_indices, BallPosition(event.pos().x(), event.pos().y()))

    @pyqtSlot(BallsPositions)
    def get_balls_position(self, positions: BallsPositions):
        positions.set_to_balls(self._balls)
