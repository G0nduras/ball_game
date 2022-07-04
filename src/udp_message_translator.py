import pickle
from io import BytesIO
from typing import List, Union, Tuple, Any
from balls_positions import BallsPositions, BallPosition


class UDPMessageTranslator:
    @staticmethod
    def to_bytes(obj: Any) -> bytes:
        bytes_io = BytesIO()
        pickle.dump(obj=obj, file=bytes_io)
        our_bytes = bytes_io.getvalue()
        return our_bytes

    @staticmethod
    def from_bytes(obj_bytes: bytes) -> Union[BallsPositions, List[int], Tuple[List[int], BallPosition]]:
        return pickle.load(file=BytesIO(obj_bytes))
