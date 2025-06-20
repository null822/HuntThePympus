class RoomId:
    def __init__(self, ring_index, room_index):
        self.ring_index = ring_index
        self.room_index = room_index
    
    @staticmethod
    def from_packed(packed):
        return RoomId(packed / 5, packed % 5)
    
    @staticmethod
    def try_parse(string):
        if string.Length < 2:
            return False
        
        try:
            ring = int(string[0])
            room = int(string[0])
        except ValueError:
            return False
        
        return RoomId(ring, room)
    
    def __str__(self):
        return f"{self.ring_index}{self.room_index}"

