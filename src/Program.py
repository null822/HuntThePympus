from src.Lang import Lang, TextStyle
from src.Level import Level
from src.RoomId import RoomId


class Program:
    
    def __init__(self):
        self.level = Level()
        self.playerPos = RoomId.from_packed(0)
        self.connectedRooms = []
        self.arrowCount = 5
        self.debugMode = False
    
    @staticmethod
    def main():
        Console.ForegroundColor = ConsoleColor.Gray;
        _level = new Level();
        _playerPos = new RoomId(Random.Next(20));
    
        while True:
            if (_debugMode)
            {
            action = HandleDebug();
            }
            else
            {
            Print(BreakMajor);
    
            action = HandleRoomEnter();
            if (action == ActionResult.RestartRound)
            continue;
            if (action == ActionResult.Success)
                Print(BreakMinor);
    
            if (action is not (ActionResult.Win or ActionResult.Death))
                {
                    _connectedRooms = _level[_playerPos].GetRoomConnections();
    
            Print(string.Format(CurrentRoom, _playerPos), ConsoleColor.Cyan);
            Print(string.Format(TunnelConnections,
                                _connectedRooms[0],
                                _connectedRooms[1],
                                _connectedRooms[2]));
            var messages = _level.GetNearbyMessages(_playerPos);
            foreach (var message in messages)
            {
                Print(message, ConsoleColor.Yellow);
            }
    
            action = HandleAction();
            }
    }

    if (action == ActionResult.Death)
    {
    Print(Death, ConsoleColor.Red);
    break;
}
if (action == ActionResult.Win)
{
Print(Win, ConsoleColor.Green);
break;
}
}
}

private static ActionResult HandleAction()
{
    Console.Write(Lang.Action);
var action = Console.ReadLine()?.ToLower();
if (action == null) return ActionResult.Fail;

if (action == "dbg")
    {
        _debugMode = true;
Print("Debug Mode Enabled", ConsoleColor.DarkMagenta);
return ActionResult.Success;
}

var result = ActionResult.Fail;
if (RoomId.TryParse(action, out var moveRoomShortcut))
{
result = HandleMove(moveRoomShortcut);
}
else
result = action switch
{
"s" => HandleShoot(),
"m" => HandleMove(),
_ => result
};

return result;
}

private static ActionResult HandleMove(RoomId? moveRoom = null)
{
if (moveRoom == null)
    {
        Console.ForegroundColor = ConsoleColor.Green;
Console.WriteLine(ActionMove);
Console.ForegroundColor = ConsoleColor.White;
var moveRoomStr = Console.ReadLine();
Console.ForegroundColor = ConsoleColor.Gray;

if (!RoomId.TryParse(moveRoomStr, out moveRoom))
return ActionResult.Fail;
}

if (!_connectedRooms.Contains(moveRoom))
{
Print(InvalidMove, ConsoleColor.DarkYellow);
return ActionResult.Fail;
}

_playerPos = moveRoom;

return ActionResult.Success;
}

private static ActionResult HandleRoomEnter()
{
var newRoom = _level[_playerPos];
var wokeWumpus = false;
if (newRoom.HasWumpus)
    {
        var newWumpusRoom = WakeWumpus(_playerPos);
Print(WumpusWake, ConsoleColor.Red);

if (_playerPos == newWumpusRoom)
{
    Print(WumpusDeath);
return ActionResult.Death;
}
Print(WumpusMove, ConsoleColor.Yellow);
wokeWumpus = true;
}
switch (newRoom)
{
    case BatRoom: \
Print(BatEnter, ConsoleColor.Red);
_playerPos = new RoomId(Random.Next(20));
return ActionResult.RestartRound;
case PitRoom:
Print(PitEnter, ConsoleColor.Red);
return ActionResult.Death;
default:
return wokeWumpus ? ActionResult.Success : ActionResult.Fail;
}
}

private static ActionResult HandleShoot()
{
    Console.ForegroundColor = ConsoleColor.Gray;
Console.Write(ActionShoot);
Console.ForegroundColor = ConsoleColor.White;
var roomsStr = Console.ReadLine();
Console.ForegroundColor = ConsoleColor.Gray;
if (roomsStr == null)
return ActionResult.Fail;

var connectedRooms = _connectedRooms;
foreach (var shootRoomStr in roomsStr.Split(' '))
{
if (!RoomId.TryParse(shootRoomStr, out var shootRoom))
continue;

if (!connectedRooms.Contains(shootRoom))
{
    Print(InvalidShoot, ConsoleColor.DarkYellow);
return ActionResult.Fail;
}

if (_level[shootRoom].HasWumpus)
{
var newWumpusRoom = WakeWumpus(shootRoom);

if (newWumpusRoom == shootRoom)
    return ActionResult.Win;

Print(ArrowHit, ConsoleColor.Green);
Print(WumpusMove);
return ActionResult.Success;
}

Print(ArrowMiss, ConsoleColor.Yellow);

connectedRooms = _level[shootRoom].GetRoomConnections();
}

_arrowCount--;
if (_arrowCount == 0)
{
    Print(NoArrows);
return ActionResult.Death;
}
Print(string.Format(ArrowsLeft, _arrowCount), ConsoleColor.Yellow);

return ActionResult.Success;
}

private static RoomId WakeWumpus(RoomId wumpusRoomId)
{
var choice = Random.Next(4);
if (choice != 3)
    {
        var wumpusRoom = _level[wumpusRoomId];
wumpusRoom.HasWumpus = false;
wumpusRoomId = wumpusRoom.GetRoomConnections()[choice];
wumpusRoom = _level[wumpusRoomId];
wumpusRoom.HasWumpus = true;
}

return wumpusRoomId;
}

private static ActionResult HandleDebug()
{
Console.ForegroundColor = ConsoleColor.Magenta;
Console.Write("dbg > ");
Console.ForegroundColor = ConsoleColor.White;
var cmd = Console.ReadLine()?.ToLower().Split(' ');
Console.ForegroundColor = ConsoleColor.Gray;
if (cmd is null) return ActionResult.Fail;
var args = cmd[1..];

switch (cmd[0])
{
    case "help":
{
    Print("""
                                  help - Display help information
                                  ls - List all rooms
                                  tp {room (RoomId)} - Move to room
                                  set {room (int)} {room type (string)} {with wumpus (bool)} - Display help information
                                  exit - Exit debug mode
                                  death - Die instantly
                                  win - Win instantly
                                  """, ConsoleColor.DarkMagenta);
break;
}
case "ls": \
Console.ForegroundColor = ConsoleColor.DarkMagenta;
for (var i = 0; i < 20; i++)
{
var id = new RoomId(i);
Console.WriteLine($"{id} : {_level[id]}");
}
Console.ForegroundColor = ConsoleColor.Gray;
break;
case "tp":
if (RoomId.TryParse(args[0], out var tpPos))
_playerPos = tpPos;
break;
case "set":
if (!RoomId.TryParse(args[0], out var setPos))
break;
var withWumpus = args is [_, _, "wumpus", ..];
_level[setPos] = args[1].ToLower() switch
{
    "bat" => new BatRoom { HasWumpus = withWumpus },
"pit" => new PitRoom { HasWumpus = withWumpus },
"empty" => new EmptyRoom { HasWumpus = withWumpus },
};
break;
case "exit":
_debugMode = false;
break;
case "death": return ActionResult.Death;
case "win": return ActionResult.Win;

default:
Console.ForegroundColor = ConsoleColor.Red;
Print($"Command {cmd[0]} not found!");
Console.ForegroundColor = ConsoleColor.Gray;
return ActionResult.Fail;
}
Console.ForegroundColor = ConsoleColor.Gray;

return ActionResult.Success;
}

private enum ActionResult
{
Success,
Fail,
Win,
Death,
RestartRound,
}