from typing import List
from PyQt6.QtCore import QPointF, Qt, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QGraphicsScene
from src.network.balls_positions import BallsPositionsMessage, BallPosition
from src.network.targets_for_balls_message import TargetsForBallsMessage
from src.network.jump_message import JumpMessage
from client_player import ClientPlayer
from client_ball import ClientBall
from selecting_rect import SelectingRect


class ClientScene(QGraphicsScene):
    jump_signal = pyqtSignal(JumpMessage)
    set_target_signal = pyqtSignal(TargetsForBallsMessage)

    def __init__(
            self,
            client_players: List[ClientPlayer],
            player_id: int
    ):
        super().__init__()
        self._client_players: List[ClientPlayer] = client_players
        self._selected_balls: List[ClientBall] = []
        self._selecting_rect: SelectingRect = SelectingRect()
        self._player_id = player_id

        for player in client_players:
            for ball in player.balls:
                ball.add_ball_to_scene(self)

        self._selecting_rect.add_rect_to_scene(self)

    def key_press_event(self, event):
        if event.key() == Qt.Key.Key_Space:
            player = self._client_players[self._player_id]
            ball_indices = [
                ball_index
                for ball_index, ball in enumerate(player.balls)
                if ball in self._selected_balls
            ]
            jump_message = JumpMessage(ball_indices=ball_indices, player_indices=self._player_id)
            self.jump_signal.emit(jump_message)

    def mouse_move_event(self, event):
        if not self._selecting_rect.is_none():
            self._selecting_rect.expand_rect(event.pos())

    def mouse_release_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            player = self._client_players[self._player_id]
            if self._selecting_rect.is_small():
                for player in self._client_players:
                    for ball in player.balls:
                        if ball.is_clicked(mouse_position=QPointF(event.pos())):
                            self._selected_balls = [ball]
                            break
                else:
                    self._selected_balls = []
            else:
                self._selected_balls = self._selecting_rect.filter_selected_balls(player.balls)
            for player in self._client_players:
                for ball in player.balls:
                    ball.set_draw_method(is_selected=ball in self._selected_balls)
                self._selecting_rect.clear_rect()

    def mouse_press_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self._selecting_rect.start_rect(event.pos())
        if event.buttons() == Qt.MouseButton.RightButton:
            player = self._client_players[self._player_id]
            if self._selected_balls is not None:
                ball_indices = [
                    ball_index
                    for ball_index, ball in enumerate(player.balls)
                    if ball in self._selected_balls
                ]
                targets = TargetsForBallsMessage(
                    indices=ball_indices,
                    position=BallPosition(event.pos().x(), event.pos().y()),
                    player_id=self._player_id
                )
                self.set_target_signal.emit(targets)

    @pyqtSlot(BallsPositionsMessage)
    def get_balls_position(self, positions: BallsPositionsMessage):
        positions.set_to_players(self._client_players)
