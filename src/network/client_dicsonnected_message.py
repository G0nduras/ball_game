from dataclasses import dataclass


@dataclass
class ClientDisconnectedMessage:
    player_id: int
