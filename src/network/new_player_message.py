from dataclasses import dataclass


@dataclass
class NewPlayerMessage:
    player_id: int
    spawn_x: int
    spawn_y: int
    radius: int
    default_color: str
