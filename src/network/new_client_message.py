from dataclasses import dataclass

from src.network.new_player_message import NewPlayerMessage


@dataclass
class NewClientMessage:
    spawn_x: int
    spawn_y: int
    default_color: str
    radius: int
    udp_host: str
    udp_port: int
    tcp_host: str
    tcp_port: int

    def to_new_player_message(self, player_id: int) -> NewPlayerMessage:
        return NewPlayerMessage(
            player_id=player_id,
            spawn_x=self.spawn_x,
            spawn_y=self.spawn_y,
            default_color=self.default_color,
            radius=self.radius,
        )
