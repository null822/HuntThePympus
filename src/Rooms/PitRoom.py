from src.Lang import Lang
from src.Room import Room


class PitRoom(Room):
    def __init__(self):
        super().__init__()
        self.type: str = "Pit"
    
    def add_messages(self, messages: list[str]) -> None:
        super().add_messages(messages)
        messages.append(Lang.pit_nearby)
