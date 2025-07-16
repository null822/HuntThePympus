import random

from src.Lang import Lang, TextStyle
from src.Level import Level
from src.RoomId import RoomId
from src.Rooms.BatRoom import BatRoom
from src.Rooms.EmptyRoom import EmptyRoom
from src.Rooms.PitRoom import PitRoom

class Program:
    
    level: Level = Level()
    player_pos: RoomId = RoomId.from_packed(random.randint(0, 20))
    connected_rooms: list[RoomId] = []
    arrow_count: int = 5
    debug_mode: bool = False
    
    @staticmethod
    def main():
        while True:
            if Program.debug_mode:
                action = Program.handle_debug()
            else:
                Lang.print(Lang.break_major)
                
                action = Program.handle_room_enter()
                if action == "RestartRound":
                    continue
                
                if action == "Success":
                    Lang.print(Lang.break_minor)
                
                if action != "Win" and action != "Death":
                    Program.connected_rooms = Program.player_pos.get_room_connections()
                    
                    Lang.print(Lang.current_room.format(pos=Program.player_pos), TextStyle.fCyan)
                    Lang.print(Lang.tunnel_connections.format(
                        r0 = Program.connected_rooms[0],
                        r1 = Program.connected_rooms[1],
                        r2 = Program.connected_rooms[2]))
                    messages = Program.level.get_nearby_messages(Program.player_pos)
                    for message in messages:
                        Lang.print(message, TextStyle.fYellow)
                    
                    
                    action = Program.handle_action()
            
            if action == "Death":
                Lang.print(Lang.death, TextStyle.fRed)
                break
            if action == "Win":
                Lang.print(Lang.win, TextStyle.fGreen)
                break

    @staticmethod
    def handle_action():
        action = input(Lang.action).lower()
        if action is None:
            return "Fail"
        
        if action == "dbg":
            Program.debug_mode = True
            Lang.print("Debug Mode Enabled", TextStyle.fDarkMagenta)
            return "Success"
        
        result = "Fail"
        move_room_shortcut = RoomId.try_parse(action)
        if move_room_shortcut is not None:
            result = Program.handle_move(move_room_shortcut)
        else:
            match action:
                case "s": Program.handle_shoot(),
                case "m": Program.handle_move(),
                case _: 
                    Lang.print(Lang.invalid_action, TextStyle.fDarkYellow)
            
        return result
    
    @staticmethod
    def handle_move(move_room = None):
        if move_room is None:
            Lang.print(Lang.action_move, TextStyle.fGreen, '')
            move_room_str = input()
            move_room = RoomId.try_parse(move_room_str)
            if move_room is None:
                Lang.print(Lang.invalid_room, TextStyle.fDarkYellow)
                return "Fail"
        
        if not move_room in Program.connected_rooms:
            Lang.print(Lang.invalid_move, TextStyle.fDarkYellow)
            return "Fail"
        
        Program.player_pos = move_room
        return "Success"
        
    @staticmethod
    def handle_room_enter():
        new_room = Program.level[Program.player_pos]
        woke_wumpus = False
        if new_room.has_wumpus:
            new_wumpus_room = Program.wake_wumpus(Program.player_pos)
            Lang.print(Lang.wumpus_wake, TextStyle.fRed)
            
            if Program.player_pos == new_wumpus_room:
                Lang.print(Lang.wumpus_death)
                return "Death"
            Lang.print(Lang.wumpus_move, TextStyle.fYellow)
            woke_wumpus = True
        
        if type(new_room) is BatRoom:
            Lang.print(Lang.bat_enter, TextStyle.fRed)
            Program.player_pos = RoomId.from_packed(random.randint(0, 20))
            return "RestartRound"
        elif type(new_room) is PitRoom:
            Lang.print(Lang.pit_enter, TextStyle.fRed)
            return "Death"
        else:
            return "Success" if woke_wumpus else "Fail"
    
    @staticmethod
    def handle_shoot():
        print("shoot")
        Lang.print(Lang.action_shoot, TextStyle.fGreen, '')
        rooms_str = input()
        if rooms_str is None:
            return "Fail"
        
        connected_rooms = Program.connected_rooms
        for shootRoomStr in rooms_str.split(' '):
            shoot_room = RoomId.try_parse(shootRoomStr)
            if shoot_room is None:
                continue
            
            if not shoot_room in connected_rooms:
                Lang.print(Lang.invalid_shoot, TextStyle.fDarkYellow)
                return "Fail"
            
            if Program.level[shoot_room].has_wumpus:
                new_wumpus_room = Program.wake_wumpus(shoot_room)
                
                if new_wumpus_room == shoot_room:
                    return "Win"
                
                Lang.print(Lang.arrow_hit, TextStyle.fGreen)
                Lang.print(Lang.wumpus_move)
                print(f"{shoot_room} -> {new_wumpus_room}")
                return "Success"
            
            Lang.print(Lang.arrow_miss, TextStyle.fYellow)
            connected_rooms = Program.level[shoot_room].id.get_room_connections()
        
        Program.arrow_count = Program.arrow_count - 1
        if Program.arrow_count == 0:
            Lang.print(Lang.no_arrows)
            return "Death"
        
        Lang.print(Lang.arrows_left.format(count=Program.arrow_count), TextStyle.fYellow)
        
        return "Success"
    
    @staticmethod
    def wake_wumpus(wumpus_room_id):
        choice = random.randint(0, 4)
        if choice != 3:
            wumpus_room = Program.level[wumpus_room_id]
            wumpus_room.has_wumpus = False
            wumpus_room_id = wumpus_room.id.get_room_connections()[choice]
            wumpus_room = Program.level[wumpus_room_id]
            wumpus_room.has_wumpus = True
        
        return wumpus_room_id
    
    @staticmethod
    def handle_debug() -> str:
        Lang.print("dbg > ", TextStyle.fMagenta, '')
        cmd = input().lower().split(' ')
        
        if cmd is None: return "Fail"
        args = cmd[1:]
        
        match cmd[0]:
            case "help":
                Lang.print(
"""    help - Display help information
    ls - List all rooms
    tp {room (RoomId)} - Move to room
    set {room (int)} {room type (string)} {with wumpus (bool)} - Display help information
    exit - Exit debug mode
    death - Die instantly
    win - Win instantly""", TextStyle.fDarkMagenta)
            case "ls":
                for i in range(20):
                    id = RoomId.from_packed(i)
                    Lang.print(f"{id} : {Program.level[id]}", TextStyle.fDarkMagenta)
            case "tp":
                if len(args) > 0:
                    tp_pos = RoomId.try_parse(args[0])
                    if tp_pos is not None:
                        Program.player_pos = tp_pos
            case "set":
                if len(args) > 2:
                    set_pos = RoomId.try_parse(args[0])
                    if set_pos is not None:
                        with_wumpus = (len(args) >= 3) & (args[2] == "wumpus")
                        match args[1].lower():
                            case "bat": 
                                r = BatRoom()
                                r.has_wumpus = with_wumpus
                                Program.level[set_pos] = r
                            case "pit":
                                r = PitRoom()
                                r.has_wumpus = with_wumpus
                                Program.level[set_pos] = r
                            case "empty":
                                r = EmptyRoom()
                                r.has_wumpus = with_wumpus
                                Program.level[set_pos] = r
            case "exit":
                Program.debug_mode = False
            case "death": return "Death"
            case "win": return "Win"
            case _:
                Lang.print(f"Command {cmd[0]} not found!", TextStyle.fRed)
                return "Fail"
        
        return "Success"

if __name__ == "__main__":
    Program.main()