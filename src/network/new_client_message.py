from dataclasses import dataclass


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
