import sys
from omegaconf import OmegaConf
from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtWidgets import QApplication
from net_address import NetAddress
from server_ball import ServerBall
from server_scene import ServerScene
from udp_handler import UDPHandler
from server_player import ServerPlayer


PLAYERS_COUNT = 2
SERVER_CONFIG_PATH = "server_config.yaml"
REMOTE_CLIENT_IP = "127.0.0.1"


def run_server():
    app = QApplication(sys.argv)
    conf = OmegaConf.load(SERVER_CONFIG_PATH)
    players = [
        ServerPlayer(players_id=0, balls=[ServerBall(
            x=400,
            y=350,
            radius=75,
            density=conf.density,
            resistance_alpha=conf.resistance_alpha,
            thrust_force_module=conf.trust_force_module,
            jump_impulse_module=conf.impulse_module,
        )]),
        ServerPlayer(players_id=1, balls=[ServerBall(
            x=400 * 2,
            y=350,
            radius=75,
            density=conf.density,
            resistance_alpha=conf.resistance_alpha,
            thrust_force_module=conf.trust_force_module,
            jump_impulse_module=conf.impulse_module,
        )]),
    ]
    server_scene = ServerScene(server_players=players, frame_per_second=60)
    server_udp_handler = UDPHandler(
        listening_net_addresses=[
            NetAddress(host=QHostAddress.SpecialAddress.LocalHost, port=12340),
            NetAddress(host=QHostAddress.SpecialAddress.LocalHost, port=12341),
        ],
        target_net_addresses=[
            NetAddress(host=QHostAddress.SpecialAddress.LocalHost, port=12342),
            NetAddress(host=QHostAddress(REMOTE_CLIENT_IP), port=12343),
        ],
    )
    server_udp_handler.jump_signal.connect(server_scene.set_jump)
    server_udp_handler.set_target_signal.connect(server_scene.set_target_for_selected_balls)
    server_scene.set_pos_signal.connect(server_udp_handler.send_obj)
    sys.exit(app.exec())


if __name__ == "__main__":
    run_server()
