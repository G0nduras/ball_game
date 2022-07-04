import sys

from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtWidgets import QApplication
from server_ball import ServerBall
from server_scene import ServerScene
from udp_handler import UDPHandler


def run_server():
    app = QApplication(sys.argv)
    impulse_module = 50000000
    trust_force_module = 100000
    resistance_alpha = 50
    density = 1
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
    server_udp_handler = UDPHandler(
        target_port=7777,
        listening_port=8888,
        target_host=QHostAddress.SpecialAddress.LocalHostIPv6,
        listening_host=QHostAddress.SpecialAddress.LocalHostIPv6,
    )
    server_udp_handler.jump_signal.connect(server_scene.set_jump)
    server_udp_handler.set_target_signal.connect(server_scene.set_target_for_selected_balls)
    server_scene.set_pos_signal.connect(server_udp_handler.send_obj)
    sys.exit(app.exec())


if __name__ == "__main__":
    run_server()
