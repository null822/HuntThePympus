import random

from src.ExclusiveRngSelector import ExclusiveRngSelector
from src.Room import Room
from src.RoomId import RoomId
from src.Rooms.BatRoom import BatRoom
from src.Rooms.EmptyRoom import EmptyRoom
from src.Rooms.PitRoom import PitRoom

class Level:
    
    def __init__(self):
        self.rooms = [[Room()]*4]*5 # 4 rings per level, 5 rooms per ring
        
        wumpus_room = RoomId.from_packed(random.randint(0, 20))
        room_selector = ExclusiveRngSelector()
        bat_rooms = [
            RoomId.from_packed(room_selector.next(20)),
            RoomId.from_packed(room_selector.next(20)),
        ]
        pit_rooms = [
            RoomId.from_packed(room_selector.next(20)),
            RoomId.from_packed(room_selector.next(20))
        ]
        
        for ringIndex in range(0, 4):
            for roomIndex in range(0, 4):
                
                id = RoomId(ringIndex, roomIndex)
                
                if any(r = id for (_, _, r) in bat_rooms):
                    room = BatRoom()
                elif any(r = id for (_, _, r) in pit_rooms):
                    room = PitRoom()
                else:
                    room = EmptyRoom()
                
                room.HasWumpus = id == wumpus_room
                
                room.id = id
                self.rooms[ringIndex][roomIndex] = room

    def get(self, id):
        return self.rooms[id.RingIndex][id.RoomIndex]
    def set(self, id, value):
        self.set_room(value, id)
    
    def set_room(self, room, id):
        room.id = id
        self.rooms[id.RingIndex][id.RoomIndex] = room


    def get_nearby_messages(self, room):
        
        messages = []
        for roomConnection in self.get(room).get_room_connections():
            connected_room = self.get(roomConnection)
            connected_room.add_messages(messages)
        return messages
