class Lang:

    break_major = "================================"
    break_minor = "--------------------------------"

    current_room = "You are in Room {0}"
    tunnel_connections = "Tunnels lead to Rooms {0}, {1}, {2}"

    action = "Shoot or Move (S/M) ? "
    action_move = "Where To? "
    action_shoot = "Which Room? "

    invalidMove = "Can't get there!"
    invalidShoot = "Can't shoot there!"

    arrowsLeft = "{0} Arrows Left"
    arrowMiss = "You Missed!"
    arrowHit = "You hit the wumpus!"

    wumpusNearby = "You smell a wumpus nearby"
    batNearby = "You hear flapping nearby"
    pitNearby = "You feel a breeze nearby"

    death = "HA HA HA - YOU LOSE!"
    win = "YOU GOT THE WUMPUS!\nHEE HEE HEE - HE'LL GETCHA NEXT TIME!!"

    wumpusWake = "You woke the wumpus!"
    wumpusMove = "The wumpus ran away!"
    wumpusDeath = "...OOPS! THE WUMPUS GOT YOU!"
    pitEnter = "YYYIIIIEEEE . . . FELL IN PIT"
    batEnter = "ZAP--SUPER BAT SNATCH! ELSEWHEREVILLE FOR YOU!"
    noArrows = "YOU'VE RUN OUT OF ARROWS!"
    
    @staticmethod
    def print(s, color = "39;49;"):
        color = color[:len(color)-1]
        print(f"\033[0m\033[{color}m{s}\033[0m")
    
    @staticmethod
    def set_color(color):
        color = color[:len(color)-1]
        print(f"\033[0m\033[{color}m", end="")
        
class TextStyle:
    fDefault =      "39;"
    
    fBlack =        "30;"
    fGray =         "37;"
    fDarkGray =     "90;"
    fWhite =        "38;"

    fRed =          "91;"
    fGreen =        "92;"
    fYellow =       "93;"
    fBlue =         "94;"
    fMagenta =      "95;"
    fCyan =         "96;"
    
    fDarkRed =      "31;"
    fDarkGreen =    "32;"
    fDarkYellow =   "33;"
    fDarkBlue =     "34;"
    fDarkMagenta =  "35;"
    fDarkCyan =     "36;"


    bDefault =      "49;"
    
    bBlack =        "40;"
    bGray =         "47;"
    bDarkGray =     "100;"
    bWhite =        "107;"

    bRed =          "101;"
    bGreen =        "102;"
    bYellow =       "103;"
    bBlue =         "104;"
    bMagenta =      "105;"
    bCyan =         "106;"

    bDarkRed =      "41;"
    bDarkGreen =    "42;"
    bDarkYellow =   "43;"
    bDarkBlue =     "44;"
    bDarkMagenta =  "45;"
    bDarkCyan =     "46;"
    
    box =           "51;"
    
    bold =          "1;"
    italic =        "3;"
    underline =     "4;"
    strikethrough = "9;"
    