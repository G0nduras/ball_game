from typing import List, Optional
from math import sqrt
from PyQt6.QtCore import QPointF, QTimer, Qt
from PyQt6.QtGui import QVector2D
from PyQt6.QtWidgets import QGraphicsScene
from selecting_rect import SelectingRect
from ball import Ball

MIN_TARGET_DISTANCE = 2


class BallScene(QGraphicsScene):
    def __init__(
            self,
            frame_per_second: int,
            balls: List[Ball],
            selecting_rect: SelectingRect,
            widget: "BallWidget",
    ):
        super().__init__()
        self._mouse_position: Optional[QPointF] = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.one_timer_tick)
        self.timer.start(round(1000 / frame_per_second))
        self._balls: List[Ball] = balls
        self._selected_balls: List[Ball] = []
        self._selecting_rect: SelectingRect = selecting_rect
        self._widget = widget
        self._repulsive_mul = 10000

        for ball in balls:
            ball.add_ball_to_scene(self)

        selecting_rect.add_rect_to_scene(self)

    def key_press_event(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self._widget.close()
        if event.key() == Qt.Key.Key_Space:
            for ball in self._selected_balls:
                if ball._center_target is not None:
                    impulse = ball.calculate_moving_direction() * ball._impulse_score
                    ball.add_impulse(impulse)
        self.update()

    def mouse_move_event(self, event):
        if not self._selecting_rect.is_none():
            self._selecting_rect.expand_rect(event.pos())
        self._mouse_position = QPointF(event.pos())
        self.update()

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
        self.update()
        self._selecting_rect.clear_rect()

    def mouse_press_event(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self._selecting_rect.start_rect(event.pos())
        if event.buttons() == Qt.MouseButton.RightButton:
            if self._selected_balls is not None:
                for ball in self._selected_balls:
                    ball.set_center_target(center_target=QPointF(event.pos()))

    def one_timer_tick(self):
        for index_1 in range(0, len(self._balls)):
            for index_2 in range(index_1 + 1, len(self._balls)):
                ball1 = self._balls[index_1]
                ball2 = self._balls[index_2]
                if QVector2D((ball1.pos() - ball2.pos())).length() < ball1._radius + ball2._radius:
                    mass1 = ball1._mass
                    mass2 = ball2._mass
                    velocity1 = ball1._velocity
                    velocity2 = ball2._velocity
                    ball_to_ball = QVector2D(ball1.pos() - ball2.pos())
                    p_1 = mass1 * velocity1
                    p_2 = mass2 * velocity2
                    projection_p1 = QVector2D.dotProduct(p_1, ball_to_ball) * ball_to_ball.length()
                    projection_p2 = QVector2D.dotProduct(p_2, ball_to_ball) * ball_to_ball.length()
                    v_1 = projection_p1 / mass1
                    v_2 = projection_p2 / mass2
                    e_0 = (mass1 * (v_1 ** 2)) / 2 + (mass2 * (v_2 ** 2)) / 2
                    p_0 = mass1 * v_1 + mass2 * v_2
                    discriminant = sqrt(mass1 * mass2) * sqrt(2 * e_0 * (mass1 + mass2) - p_0 ** 2)
                    projection_v_1 = (p_0 * mass1 + discriminant) / (mass1 * (mass1 + mass2))
                    projection_v_2 = (p_0 * mass2 - discriminant) / (mass2 * (mass1 + mass2))
                    d = ball_to_ball / ball_to_ball.length()
                    ball1.add_impulse((mass1 * projection_v_1 - mass1 * v_1) * d / self._repulsive_mul)
                    ball2.add_impulse((mass2 * projection_v_2 - mass2 * v_2) * d / self._repulsive_mul)
        for ball in self._balls:
            force = ball.calculate_sum_force()
            assert isinstance(force, QVector2D), type(force)
            acceleration = force / ball._mass
            # F = m*a
            ball._velocity += acceleration
            # V = a => DELTA_V = a * DELTA_t
            new_pos = ball.pos() + ball._velocity.toPointF()
            if ball._center_target is not None:
                shift = QVector2D(new_pos - ball._center_target)
                if shift.length() < MIN_TARGET_DISTANCE:
                    ball._center_target = None
            ball.setPos(new_pos)
        print('-' * 100)
        for ball in self._balls:
            print(ball.pos())
        print('-' * 100)
