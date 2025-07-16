import random

from src.ExclusiveRngSelector import ExclusiveRngSelector
from src.Room import Room
from src.RoomId import RoomId
from src.Rooms.BatRoom import BatRoom
from src.Rooms.EmptyRoom import EmptyRoom
from src.Rooms.PitRoom import PitRoom

class Level:
    
    def __init__(self):
        self.rooms: list[Room] = [Room()]*20
        
        wumpus_room: RoomId = RoomId.from_packed(random.randint(0, 19))
        room_selector = ExclusiveRngSelector()
        bat_rooms = [
            RoomId.from_packed(room_selector.next(19)),
            RoomId.from_packed(room_selector.next(19)),
        ]
        pit_rooms = [
            RoomId.from_packed(room_selector.next(19)),
            RoomId.from_packed(room_selector.next(19))
        ]
        
        for ring_index in range(0, 4):
            for room_index in range(0, 5):
                id = RoomId(ring_index, room_index)
                
                if id in bat_rooms:
                    room = BatRoom()
                elif id in pit_rooms:
                    room = PitRoom()
                else:
                    room = EmptyRoom()
                
                room.has_wumpus = id == wumpus_room
                
                room.id = id
                
                self.set(RoomId(ring_index, room_index), room)
        print(self.rooms)
                
    def __getitem__(self, id: RoomId):
        return self.get(id)
    def __setitem__(self, id: RoomId, room: Room):
        self.set(id, room)
    
    def get(self, id: RoomId) -> Room:
        return self.rooms[RoomId(id.ring_index, id.room_index).as_packed()]
    def set(self, id: RoomId, room: Room):
        room.id = id
        self.rooms[RoomId(id.ring_index, id.room_index).as_packed()] = room


    def get_nearby_messages(self, room):
        messages: list[str] = []
        for roomConnection in self.get(room).id.get_room_connections():
            connected_room = self.get(roomConnection)
            connected_room.add_messages(messages)
        return messages
