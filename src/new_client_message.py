class NewClientMessage:
    def __init__(
            self,
            spawn_x: int,
            spawn_y: int,
            default_color: str,
            radius: int,
    ):
        self._spawn_x = spawn_x
        self._spawn_y = spawn_y
        self._default_color = default_color
        self._radius = radius
