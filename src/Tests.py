from src.ActionResult import ActionResult
from src.Lang import Lang, TextStyle
from src.RoomId import RoomId
from src.Rooms.BatRoom import BatRoom
from src.Rooms.EmptyRoom import EmptyRoom
from src.Rooms.PitRoom import PitRoom


class Tests:
    target = RoomId.try_parse("01")
    player_pos = RoomId.try_parse("00")
    
    
    @staticmethod
    def run(program):
        Lang.enable_print = False
        program.level.set(Tests.target, EmptyRoom())
        program.level.set(Tests.player_pos, EmptyRoom())

        Tests.move(program)
        Tests.bat_room(program)
        Tests.pit_room(program)
        Tests.wumpus_room(program)
        Tests.arrows_death(program)
        Tests.wumpus_shoot(program)
        
        Lang.enable_print = True
    
    @staticmethod
    def move(program):
        program.player_pos = Tests.player_pos
        program.level.set(Tests.target, EmptyRoom())
        program.handle_move(Tests.target)
        if program.player_pos == Tests.target:
            Lang.print("Passed: Move", TextStyle.fGreen, force=True)
        else:
            Lang.print(f"Failed: Move: {program.player_pos} != {Tests.target} -------------------- [#]", TextStyle.fRed, force=True)
            
    @staticmethod
    def bat_room(program):
        program.player_pos = Tests.player_pos
        program.level.set(Tests.player_pos, BatRoom())
        result = program.handle_room_enter()
        if result == ActionResult.restartRound and program.player_pos != Tests.player_pos:
            Lang.print("Passed: Bat Move", TextStyle.fGreen, force=True)
        else:
            Lang.print(f"Failed: Pit Death: {result} != {ActionResult.death} or {program.player_pos} != {Tests.player_pos} -------------------- [#]", TextStyle.fRed, force=True)
    
    @staticmethod
    def pit_room(program):
        program.player_pos = Tests.player_pos
        program.level.set(Tests.player_pos, PitRoom())
        result = program.handle_room_enter()
        if result == ActionResult.death:
            Lang.print("Passed: Pit Death", TextStyle.fGreen)
        else:
            Lang.print(f"Failed: Pit Death: {result} != {ActionResult.death} -------------------- [#]", TextStyle.fRed, force=True)
    
    @staticmethod
    def wumpus_room(program):
        program.player_pos = Tests.player_pos
        room = EmptyRoom()
        room.has_wumpus = True
        program.level.set(Tests.player_pos, room)
        result = program.handle_room_enter()
        if result == ActionResult.death or result == ActionResult.success:
            Lang.print("Passed: Wumpus Death", TextStyle.fGreen, force=True)
        else:
            Lang.print(f"Failed: Wumpus Death: {result} != {ActionResult.death} -------------------- [#]", TextStyle.fRed, force=True)

    @staticmethod
    def wumpus_shoot(program):
        program.player_pos = Tests.player_pos
        program.arrow_count = 2
        program.level.set(Tests.target, EmptyRoom())
        result = program.handle_shoot(Tests.target)
        if result == ActionResult.win or result == ActionResult.success:
            if program.arrow_count == 1:
                Lang.print("Passed: Wumpus Shoot", TextStyle.fGreen, force=True)
            else:
                Lang.print(f"Failed: Wumpus Shoot: {program.arrow_count} != {1} -------------------- [#]", TextStyle.fRed, force=True)
        else:
            Lang.print(f"Failed: Wumpus Shoot: {result} != ({ActionResult.win} or {ActionResult.success}) -------------------- [#]", TextStyle.fRed, force=True)

    @staticmethod
    def arrows_death(program):
        program.player_pos = Tests.player_pos
        program.arrow_count = 1
        program.level.set(Tests.target, EmptyRoom())
        result = program.handle_shoot(Tests.target)
        if result == ActionResult.death:
            if program.arrow_count == 0:
                Lang.print("Passed: No Arrows Death", TextStyle.fGreen, force=True)
            else:
                Lang.print(f"Failed: No Arrows Death: {program.arrow_count} != {0} -------------------- [#]", TextStyle.fRed, force=True)
        else:
            Lang.print(f"Failed: No Arrows Death: {result} != {0} -------------------- [#]", TextStyle.fRed, force=True)

        