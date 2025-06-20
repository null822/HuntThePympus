from src.Lang import Lang
from src.Room import Room


class PitRoom(Room):
    def __init__(self):
        super().__init__()
        self.type = "Pit"
    
    def add_messages(self, messages):
        super().add_messages(messages)
        messages.Add(Lang.pitNearby)
