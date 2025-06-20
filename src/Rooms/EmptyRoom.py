from src.Room import Room


class EmptyRoom(Room):
    def __init__(self):
        super().__init__()
        self.type = "Empty"
