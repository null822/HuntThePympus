class Lang:
    
    break_major = "================================"
    break_minor = "--------------------------------"

    current_room = "You are in position {pos}"
    tunnel_connections = "Pathways lead to positions {r0}, {r1}, {r2}"

    action = "Shoot or Move (S/M) ? "
    action_move = "Where position? "
    action_shoot = "Which position? "

    invalid_room = "Invalid position!"
    invalid_action = "Invalid Action!"
    invalid_move = "Can't get there!"
    invalid_shoot = "Can't shoot there!"

    arrows_left = "{count} Bullets Left"
    arrow_miss = "You Missed!"
    arrow_hit = "You hit the Viet Cong soldier!"

    wumpus_nearby = "You hear leaves rustling nearby"
    bat_nearby = "You see one of your tunnels nearby"
    pit_nearby = "Your friends warn you of a trap nearby"

    death = "(something)"
    win = "YOU GOT THE VIET CONG SOLDIER!!"

    wumpus_wake = "You got the attention of the Viet Cong solder!"
    wumpus_move = "The Viet Cong soldier ran away"
    wumpus_death = "THE VIET CONG SOLDIER YOU GOT YOU!!"
    pit_enter = "You fell in a trap!"
    bat_enter = "A fellow soldier signals you to climb down into the tunnel"
    no_arrows = "YOU'VE RUN OUT OF BULLETS!"
    
    @staticmethod
    def print(s, color = "39;49;", end='\n'):
        color = color[:len(color)-1]
        print(f"\033[0m\033[{color}m{s}\033[0m", end=end)
    
    
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
    