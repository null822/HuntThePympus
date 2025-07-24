import random

from src.ActionResult import ActionResult
from src.Lang import Lang, TextStyle
from src.Level import Level
from src.RoomId import RoomId
from src.Rooms.BatRoom import BatRoom
from src.Rooms.EmptyRoom import EmptyRoom
from src.Rooms.PitRoom import PitRoom


class Program:
    """
    The main program
    """
    level: Level = Level()
    player_pos: RoomId = RoomId.from_packed(random.randint(0, 19))
    connected_rooms: list[RoomId] = []
    arrow_count: int = 5
    debug_mode: bool = False

    @staticmethod
    def main():
        """
        The program entrypoint
        """
        while True:
            if Program.debug_mode:
                action = Program.handle_debug()
            else:
                Lang.print(Lang.break_major)

                action = Program.handle_room_enter()
                if action == ActionResult.restartRound:
                    continue

                if action == ActionResult.success:
                    Lang.print(Lang.break_minor)

                if action != ActionResult.win and action != ActionResult.death:
                    Program.connected_rooms = Program.player_pos.get_room_connections()

                    Lang.print(Lang.current_room.format(pos=Program.player_pos), TextStyle.fCyan)
                    Lang.print(Lang.tunnel_connections.format(
                        r0=Program.connected_rooms[0],
                        r1=Program.connected_rooms[1],
                        r2=Program.connected_rooms[2]))
                    messages = Program.level.get_nearby_messages(Program.player_pos)
                    for message in messages:
                        Lang.print(message, TextStyle.fYellow)
                    
                    action = Program.handle_action()

            if action == ActionResult.death:
                Lang.print(Lang.death, TextStyle.fRed)
                break
            if action == ActionResult.win:
                Lang.print(Lang.win, TextStyle.fGreen)
                break

    @staticmethod
    def handle_action() -> int:
        """
        Gets an input from the user and handles it, returning the result
        """
        action = input(Lang.action).lower().split(' ')
        if action is None:
            return ActionResult.fail
        
        if action[0] == "dbg":
            Program.debug_mode = True
            Lang.print("Debug Mode Enabled", TextStyle.fDarkMagenta)
            return ActionResult.success
        
        match action[0]:
            case "s":
                result = Program.handle_shoot(action[1:] if len(action) > 0 else None),
            case "m":
                result = Program.handle_move(RoomId.try_parse(action[1]) if len(action) > 0 else None),
            case _:
                Lang.print(Lang.invalid_action, TextStyle.fDarkYellow)
                result = ActionResult.fail
        
        return result

    @staticmethod
    def handle_move(move_room: RoomId = None) -> int:
        """
        Handles a move action, returning the result
        """
        if move_room is None:
            Lang.print(Lang.action_move, TextStyle.fGreen, '')
            move_room_str = input()
            move_room = RoomId.try_parse(move_room_str)
            if move_room is None:
                Lang.print(Lang.invalid_room, TextStyle.fDarkYellow)
                return ActionResult.fail

        if not move_room in Program.connected_rooms:
            Lang.print(Lang.invalid_move, TextStyle.fDarkYellow)
            return ActionResult.fail

        Program.player_pos = move_room
        return ActionResult.success

    @staticmethod
    def handle_room_enter() -> int:
        """
        Handles entering a room, returning the result
        """
        new_room = Program.level[Program.player_pos]
        woke_wumpus = False
        if new_room.has_wumpus:
            new_wumpus_room = Program.wake_wumpus(Program.player_pos)
            Lang.print(Lang.wumpus_wake, TextStyle.fRed)
            
            if Program.player_pos == new_wumpus_room:
                Lang.print(Lang.wumpus_death)
                return ActionResult.death
            Lang.print(Lang.wumpus_move, TextStyle.fYellow)
            woke_wumpus = True

        if type(new_room) is BatRoom:
            Lang.print(Lang.bat_enter, TextStyle.fRed)
            Program.player_pos = RoomId.from_packed(random.randint(0, 20))
            return ActionResult.restartRound
        elif type(new_room) is PitRoom:
            Lang.print(Lang.pit_enter, TextStyle.fRed)
            return ActionResult.death
        else:
            return ActionResult.success if woke_wumpus else ActionResult.fail

    @staticmethod
    def handle_shoot(rooms: list[str] = None) -> int:
        """
        Handles shooting, getting user input if necessary, and returning the result
        """
        if rooms is None:
            Lang.print(Lang.action_shoot, TextStyle.fGreen, '')
            rooms = input().split(' ')
            if rooms is None:
                return ActionResult.fail
        
        prev_connections = Program.player_pos.get_room_connections()
        for shootRoomStr in rooms:
            shoot_room_id = RoomId.try_parse(shootRoomStr)
            if shoot_room_id is None:
                Lang.print(Lang.invalid_room, TextStyle.fDarkYellow)
                return ActionResult.fail
            shoot_room = Program.level[shoot_room_id]

            if not shoot_room_id in prev_connections:
                Lang.print(Lang.invalid_shoot, TextStyle.fDarkYellow)
                return ActionResult.fail

            if shoot_room.has_wumpus:
                new_wumpus_room = Program.wake_wumpus(shoot_room_id)

                if new_wumpus_room == shoot_room_id:
                    return ActionResult.win

                Lang.print(Lang.arrow_hit, TextStyle.fGreen)
                Lang.print(Lang.wumpus_move)
                print(f"{shoot_room_id} -> {new_wumpus_room}")
                return ActionResult.success
            
            Lang.print(Lang.arrow_miss, TextStyle.fYellow)
            prev_connections = shoot_room_id.get_room_connections()

        Program.arrow_count = Program.arrow_count - 1
        if Program.arrow_count == 0:
            Lang.print(Lang.no_arrows)
            return ActionResult.death

        Lang.print(Lang.arrows_left.format(count=Program.arrow_count), TextStyle.fYellow)

        return ActionResult.success

    @staticmethod
    def wake_wumpus(wumpus_room_id) -> RoomId:
        """
        Handles waking the wumpus, returning where the wumpus moved to
        """
        choice = random.randint(0, 3)
        if choice != 3:
            wumpus_room = Program.level[wumpus_room_id]
            wumpus_room.has_wumpus = False
            wumpus_room_id = wumpus_room.id.get_room_connections()[choice]
            wumpus_room = Program.level[wumpus_room_id]
            wumpus_room.has_wumpus = True

        return wumpus_room_id

    @staticmethod
    def handle_debug() -> int:
        """
        Handles the debug utilities, getting a command from the user, running it, and returning the result
        """
        Lang.print("dbg > ", TextStyle.fMagenta, '')
        cmd = input().lower().split(' ')

        if cmd is None: return ActionResult.fail
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
            case "death":
                return ActionResult.death
            case "win":
                return ActionResult.win
            case _:
                Lang.print(f"Command {cmd[0]} not found!", TextStyle.fRed)
                return ActionResult.fail

        return ActionResult.success


if __name__ == "__main__":
    Program.main()
