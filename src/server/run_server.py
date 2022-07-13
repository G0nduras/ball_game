import sys
from omegaconf import OmegaConf
from PyQt6.QtWidgets import QApplication
from src.server.server import Server


SERVER_CONFIG_PATH = "server_config.yaml"


def run_server():
    app = QApplication(sys.argv)
    server_conf = OmegaConf.load(SERVER_CONFIG_PATH)
    server = Server(server_conf=server_conf)
    sys.exit(app.exec())


if __name__ == "__main__":
    run_server()
