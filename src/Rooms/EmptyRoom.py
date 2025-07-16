from src.Room import Room


class EmptyRoom(Room):
    def __init__(self):
        super().__init__()
        self.type: str = "Empty"
        
    def add_messages(self, messages: list[str]) -> None:
        super().add_messages(messages)