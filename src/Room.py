from abc import ABC

from src.Lang import Lang
from src.RoomId import RoomId

class Room(ABC):
    """
    Represents a room
    """
    def __init__(self):
        self.id: RoomId = RoomId(-1, -1)
        self.has_wumpus = False
        self.type: str = ""

    def add_messages(self, messages: list[str]) -> None:
        """
        Adds any messages from this room into the list of messages supplied
        """
        if self.has_wumpus:
            messages.append(Lang.wumpus_nearby)
    

    def __str__(self):
        return f"{self.type} Room" + (" with Wumpus" if self.has_wumpus else "")
    