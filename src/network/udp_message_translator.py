import pickle
from io import BytesIO
from typing import Union, Any
from src.network.balls_positions import BallsPositionsMessage
from src.network.jump_message import JumpMessage
from src.network.targets_for_balls_message import TargetsForBallsMessage


class MessageTranslator:
    @staticmethod
    def to_bytes(obj: Any) -> bytes:
        bytes_io = BytesIO()
        pickle.dump(obj=obj, file=bytes_io)
        our_bytes = bytes_io.getvalue()
        return our_bytes

    @staticmethod
    def from_bytes(obj_bytes: bytes) -> Union[BallsPositionsMessage, JumpMessage, TargetsForBallsMessage]:
        return pickle.load(file=BytesIO(obj_bytes))
