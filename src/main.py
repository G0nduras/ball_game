import sys
from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt6.QtWidgets import QApplication, QAbstractScrollArea
from server_ball import ServerBall
from client_ball import ClientBall
from ball_widget import BallWidget
from server_scene import ServerScene
from client_scene import ClientScene


def main():
    app = QApplication(sys.argv)
    impulse_module = 50000000
    trust_force_module = 100000
    resistance_alpha = 50
    density = 1
    client_balls = [
            ClientBall(
                x=200,
                y=350,
                default_color="red",
                hover_color="darkred",
                radius=100,
            ),
            ClientBall(
                x=400,
                y=350,
                default_color="blue",
                hover_color="darkblue",
                radius=75,
            ),
            ClientBall(
                x=550,
                y=350,
                default_color="green",
                hover_color="darkgreen",
                radius=50,
            ),
            ClientBall(
                x=650,
                y=350,
                default_color="orange",
                hover_color="darkorange",
                radius=25,
            ),
        ]
    server_balls = [
            ServerBall(
                x=200,
                y=350,
                radius=100,
                density=density,
                resistance_alpha=resistance_alpha,
                thrust_force_module=trust_force_module,
                jump_impulse_module=impulse_module/2,
            ),
            ServerBall(
                x=400,
                y=350,
                radius=75,
                density=density,
                resistance_alpha=resistance_alpha,
                thrust_force_module=trust_force_module,
                jump_impulse_module=impulse_module / 4,
            ),
            ServerBall(
                x=550,
                y=350,
                radius=50,
                density=density,
                resistance_alpha=resistance_alpha,
                thrust_force_module=trust_force_module,
                jump_impulse_module=impulse_module / 10,
            ),
            ServerBall(
                x=650,
                y=350,
                radius=25,
                density=density,
                resistance_alpha=resistance_alpha,
                thrust_force_module=trust_force_module / 5,
                jump_impulse_module=impulse_module / 100,
            ),
        ]
    server_scene = ServerScene(server_balls, frame_per_second=60)
    client_scene = ClientScene(client_balls)
    server_scene.on_timer_tick_signal.connect(client_scene.get_balls_position)
    client_scene.jump_signal.connect(server_scene.set_jump)
    client_scene.set_target_signal.connect(server_scene.set_target_for_selected_balls)
    widget = BallWidget(client_scene=client_scene)
    widget.setWindowTitle("BallGame")
    widget.setMouseTracking(True)
    widget.showFullScreen()
    widget_size = widget.size()
    widget.setSceneRect(QRectF(QPointF(0, 0), QSizeF(widget_size)))
    widget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContentsOnFirstShow)
    widget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
