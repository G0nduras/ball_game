import sys
from PyQt6.QtWidgets import QApplication
from client.client import Client
from omegaconf import OmegaConf


CLIENT_CONFIG_PATH = "client_config.yaml"


def run_client():
    app = QApplication(sys.argv)
    client_conf = OmegaConf.load(CLIENT_CONFIG_PATH)
    client = Client(client_conf=client_conf)
    sys.exit(app.exec())


if __name__ == "__main__":
    run_client()
