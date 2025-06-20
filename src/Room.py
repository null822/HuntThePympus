from abc import ABC

from src.Lang import Lang
from src.RoomId import RoomId

class Room(ABC):
    def __init__(self):
        self.id = RoomId(-1, -1)
        self.has_wumpus = False
        self.type = ""
    
    def get_room_connections(self):
        if self.id.ring_index is 1 or 2:
            new_ring_inter = 2 if self.id.ring_index == 1 else 1
            room_offset_inter1 = -1 if self.id.ring_index == 1 else 0
            room_offset_inter2 = 0 if self.id.ring_index == 1 else 1
        else:
            new_ring_inter = self.id.ring_index
            room_offset_inter1 = -1
            room_offset_inter2 =  1
        
        inter1 = RoomId(new_ring_inter, (self.id.room_index + room_offset_inter1 + 5) % 5)
        inter2 = RoomId(new_ring_inter, (self.id.room_index + room_offset_inter2 + 5) % 5)
        
        ring_offset = 1 if self.id.ring_index % 2 == 0 else -1
        new_ring_intra = self.id.ring_index + ring_offset
        intra = RoomId(new_ring_intra, self.id.room_index)
        
        return [inter1, inter2, intra]


    def add_messages(self, messages):
        if self.has_wumpus:
            messages.Add(Lang.wumpusNearby)
    

    def __str__(self):
        return f"{self.type} Room" + (" with Wumpus" if self.has_wumpus else "")
    