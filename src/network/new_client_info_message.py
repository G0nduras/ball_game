from dataclasses import dataclass
from typing import List

from src.network.new_player_message import NewPlayerMessage


@dataclass
class NewClientInfoMessage:
    player_id: int
    other_players: List[NewPlayerMessage]
