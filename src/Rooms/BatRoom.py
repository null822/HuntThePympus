from src.Lang import Lang
from src.Room import Room


class BatRoom(Room):
    def __init__(self):
        super().__init__()
        self.type = "Bat"
    
    def add_messages(self, messages):
        super().add_messages(messages)
        messages.Add(Lang.batNearby)
