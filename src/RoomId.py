
class RoomId:
    def __init__(self, ring_index: int, room_index: int):
        self.ring_index: int = ring_index
        self.room_index: int = room_index
    
    @staticmethod
    def from_packed(packed: int):
        return RoomId(int(packed / 5), packed % 5)
    
    @staticmethod
    def try_parse(string: str) -> 'RoomId' or None: 
        if len(string) < 2:
            return None
        
        try:
            ring = int(string[0])
            room = int(string[1])
        except ValueError:
            return None
        
        if ring >= 4 or room >= 5:
            return None
        
        return RoomId(ring, room)
    
    def as_packed(self):
        return self.ring_index * 5 + self.room_index
    
    def get_room_connections(self):
        if self.ring_index == 1 or self.ring_index == 2:
            new_ring_inter = 2 if self.ring_index == 1 else 1
            room_offset_inter1 = -1 if self.ring_index == 1 else 0
            room_offset_inter2 = 0 if self.ring_index == 1 else 1
        else:
            new_ring_inter = self.ring_index
            room_offset_inter1 = -1
            room_offset_inter2 =  1

        inter1 = RoomId(new_ring_inter, (self.room_index + room_offset_inter1 + 5) % 5)
        inter2 = RoomId(new_ring_inter, (self.room_index + room_offset_inter2 + 5) % 5)
        
        ring_offset = 1 if self.ring_index % 2 == 0 else -1
        new_ring_intra = self.ring_index + ring_offset
        intra = RoomId(new_ring_intra, self.room_index)
        
        return [inter1, inter2, intra]
    
    def __str__(self):
        return f"{self.ring_index}{self.room_index}"
    
    def __eq__(self, other):
        return self.ring_index == other.ring_index and self.room_index == other.room_index

