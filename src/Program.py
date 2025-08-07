import os
import random

from src.ActionResult import ActionResult
from src.Lang import Lang
from src.TextStyle import TextStyle
from src.Level import Level
from src.RoomId import RoomId
from src.Rooms.BatRoom import BatRoom
from src.Rooms.EmptyRoom import EmptyRoom
from src.Rooms.PitRoom import PitRoom
from src.Tests import Tests


class Program:
    """
    The main program
    """
    level: Level
    player_pos: RoomId
    arrow_count: int = 5
    debug_mode: bool = False
    round = 1
    wins = 0
    deaths = 0
    
    @staticmethod
    def main():
        """
        The program entrypoint
        """
        os.system('cls' if os.name=='nt' else 'clear')
        print()
        
        Lang.print(Lang.title, TextStyle.fGray)
        Lang.print(Lang.subtitle, TextStyle.fRed)
        Lang.print(Lang.subsubtitle, TextStyle.fMagenta)
        print()
        Lang.print(Lang.welcome)
        Lang.print(Lang.action, TextStyle.fMagenta, end='')
        
        if input().lower() == "help":
            Program.print_instructions()
        
        while True:
            Lang.print(Lang.break_major, TextStyle.fRed)
            Lang.print(Lang.start.format(r=Program.round, w=Program.wins, d=Program.deaths), TextStyle.fRed)
            
            Program.level = Level()
            Program.player_pos = RoomId.from_packed(random.randint(0, 19))
            Program.arrow_count = 5
            Program.debug_mode = False
            
            while True:
    
                if Program.debug_mode:
                    action: int = Program.handle_debug()
                else:
                    Lang.print(Lang.break_major, TextStyle.fRed)
    
                    action: int = Program.handle_room_enter()
                    if action == ActionResult.restartRound:
                        continue
    
                    if action == ActionResult.success:
                        Lang.print(Lang.break_minor)
    
                    if action != ActionResult.win and action != ActionResult.death:
                        
                        connected_rooms = Program.player_pos.get_room_connections()
                        Lang.print(Lang.current_room.format(pos=Program.player_pos), TextStyle.fCyan)
                        Lang.print(Lang.tunnel_connections.format(
                            r0=connected_rooms[0],
                            r1=connected_rooms[1],
                            r2=connected_rooms[2]))
                        messages = Program.level.get_nearby_messages(Program.player_pos)
                        for message in messages:
                            Lang.print(message, TextStyle.fYellow)
                        
                        action: int = Program.handle_action()
    
                if action == ActionResult.death:
                    Lang.print(Lang.death, TextStyle.fRed)
                    Program.deaths += 1
                    break
                if action == ActionResult.win:
                    Lang.print(Lang.win, TextStyle.fGreen)
                    Program.wins += 1
                    break
            
            Lang.print(Lang.new_round, TextStyle.fWhite, end='')
            if input().lower() == 'n':
                break
            
            Program.round += 1

    @staticmethod
    def handle_action() -> int:
        """
        Gets an input from the user and handles it, returning the result
        """
        Lang.print(Lang.action, TextStyle.fMagenta, end='')
        action = input().lower().split(' ')
        if action is None:
            return ActionResult.fail
        
        match action[0]:
            case "s":
                result: int = Program.handle_shoot(RoomId.try_parse(action[1]) if len(action) > 1 else None)
            case "m":
                result: int = Program.handle_move(RoomId.try_parse(action[1]) if len(action) > 1 else None)
            case "dbg":
                Program.debug_mode = True
                Lang.print("Debug Mode Enabled", TextStyle.fDarkMagenta)
                result: int = ActionResult.success
            case _:
                move_room = RoomId.try_parse(action[0])
                if move_room is not None:
                    result: tuple[int] = Program.handle_move(move_room),
                else:
                    Lang.print(Lang.invalid_action, TextStyle.fRed)
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
                Lang.print(Lang.invalid_room, TextStyle.fRed)
                return ActionResult.fail

        if not move_room in Program.player_pos.get_room_connections():
            Lang.print(Lang.invalid_move, TextStyle.fRed)
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
                Lang.print(Lang.wumpus_death, TextStyle.fRed)
                return ActionResult.death
            Lang.print(Lang.wumpus_move, TextStyle.fYellow)
            woke_wumpus = True

        if type(new_room) is BatRoom:
            Lang.print(Lang.bat_enter, TextStyle.fGreen)
            packed_room = random.randint(0, 18) # any room except the current one
            if packed_room >= Program.player_pos.as_packed():
                packed_room += 1
            Program.player_pos = RoomId.from_packed(packed_room)
        
            return ActionResult.restartRound
        elif type(new_room) is PitRoom:
            Lang.print(Lang.pit_enter, TextStyle.fRed)
            return ActionResult.death
        else:
            return ActionResult.success if woke_wumpus else ActionResult.fail

    @staticmethod
    def handle_shoot(shoot_room_id: RoomId = None) -> int:
        """
        Handles shooting, getting user input if necessary, and returning the result
        """
        if shoot_room_id is None:
            Lang.print(Lang.action_shoot, TextStyle.fGreen, '')
            shoot_room_id = input()
            if shoot_room_id is None:
                return ActionResult.fail
        
        # arrow count
        Program.arrow_count = Program.arrow_count - 1
        Lang.print(Lang.arrows_left.format(count=Program.arrow_count), TextStyle.fRed)
        
        if shoot_room_id is None:
            Lang.print(Lang.invalid_room, TextStyle.fRed)
            return ActionResult.fail
        shoot_room = Program.level[shoot_room_id]
        
        # can't reach room
        if not shoot_room_id in Program.player_pos.get_room_connections():
            Lang.print(Lang.invalid_shoot, TextStyle.fRed)
            return ActionResult.fail
        
        # hit wumpus
        if shoot_room.has_wumpus:
            new_wumpus_room = Program.wake_wumpus(shoot_room_id)
            
            if new_wumpus_room == shoot_room_id:
                return ActionResult.win
            
            Lang.print(Lang.wumpus_move, TextStyle.fYellow)
            
            if Program.arrow_count == 0:
                Lang.print(Lang.no_arrows, TextStyle.fRed)
                return ActionResult.death
            return ActionResult.success
        
        Lang.print(Lang.arrow_miss.format(r=shoot_room_id), TextStyle.fYellow)

        if Program.arrow_count == 0:
            Lang.print(Lang.no_arrows, TextStyle.fRed)
            return ActionResult.death
        return ActionResult.success

    @staticmethod
    def wake_wumpus(wumpus_room_id) -> RoomId:
        """
        Handles waking the wumpus, returning where the wumpus moved to
        """
        win = random.randint(1, 100)
        if win <= 25:
            wumpus_room = Program.level[wumpus_room_id]
            wumpus_room.has_wumpus = False
            wumpus_room_id = wumpus_room.id.get_room_connections()[random.randint(0, 2)]
            wumpus_room = Program.level[wumpus_room_id]
            wumpus_room.has_wumpus = True

        return wumpus_room_id

    @staticmethod
    def print_instructions():
        Lang.print(Lang.break_major, TextStyle.fWhite)
        Lang.print("Instructions", TextStyle.fCyan)
        Lang.print("Find (and kill) the Viet Cong Soldier", TextStyle.fWhite)
        
        Lang.print("\nmove around by typing:", TextStyle.fWhite)
        Lang.print("!> m [new position]", TextStyle.fGreen)
        Lang.print("shoot by typing:", TextStyle.fWhite)
        Lang.print("!> s [target position]", TextStyle.fGreen)
        
        Lang.print("\nBe careful, there are traps around, and the enemy can fight back!", TextStyle.fRed)
        
    @staticmethod
    def handle_debug() -> int:
        """
        Handles the debug utilities, getting a command from the user, running it, and returning the result
        """
        Lang.print("dbg !> ", TextStyle.fMagenta, '')
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
    win - Win instantly
    test - Run the unit tests and exit""", TextStyle.fDarkMagenta)
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
            case "test":
                Tests.run(Program)
                return ActionResult.win
            case _:
                Lang.print(f"Command {cmd[0]} not found!", TextStyle.fRed)
                return ActionResult.fail

        return ActionResult.success