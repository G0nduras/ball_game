import sys
from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtWidgets import QApplication
from server_ball import ServerBall
from server_scene import ServerScene
from udp_handler import UDPHandler
from server_player import ServerPlayer

PLAYERS_COUNT = 2


def run_server():
    app = QApplication(sys.argv)
    impulse_module = 40000000
    trust_force_module = 400000
    resistance_alpha = 700
    density = 1
    players = [
        ServerPlayer(players_id=0, balls=[ServerBall(
            x=400,
            y=350,
            radius=75,
            density=density,
            resistance_alpha=resistance_alpha,
            thrust_force_module=trust_force_module,
            jump_impulse_module=impulse_module,
        )]),
        ServerPlayer(players_id=1, balls=[ServerBall(
            x=400 * 2,
            y=350,
            radius=75,
            density=density,
            resistance_alpha=resistance_alpha,
            thrust_force_module=trust_force_module,
            jump_impulse_module=impulse_module,
        )]),
    ]
    server_scene = ServerScene(server_players=players, frame_per_second=60)
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
