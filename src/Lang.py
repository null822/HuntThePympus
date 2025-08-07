
class Lang:
    
    break_major = "================================================"
    break_minor = "------------------------------------------------"
    
    title = """██╗  ██╗██╗   ██╗███╗   ██╗████████╗    ████████╗██╗  ██╗███████╗    ██╗    ██╗██╗   ██╗███╗   ███╗██████╗ ██╗   ██╗███████╗
██║  ██║██║   ██║████╗  ██║╚══██╔══╝    ╚══██╔══╝██║  ██║██╔════╝    ██║    ██║██║   ██║████╗ ████║██╔══██╗██║   ██║██╔════╝
███████║██║   ██║██╔██╗ ██║   ██║          ██║   ███████║█████╗      ██║ █╗ ██║██║   ██║██╔████╔██║██████╔╝██║   ██║███████╗
██╔══██║██║   ██║██║╚██╗██║   ██║          ██║   ██╔══██║██╔══╝      ██║███╗██║██║   ██║██║╚██╔╝██║██╔═══╝ ██║   ██║╚════██║
██║  ██║╚██████╔╝██║ ╚████║   ██║          ██║   ██║  ██║███████╗    ╚███╔███╔╝╚██████╔╝██║ ╚═╝ ██║██║     ╚██████╔╝███████║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝          ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝  ╚═════╝ ╚═╝     ╚═╝╚═╝      ╚═════╝ ╚══════╝
"""
    subtitle = """██╗   ██╗██╗███████╗████████╗     ██████╗ ██████╗ ███╗   ██╗ ██████╗     ███████╗██████╗ ██╗████████╗██╗ ██████╗ ███╗   ██╗ 
██║   ██║██║██╔════╝╚══██╔══╝    ██╔════╝██╔═══██╗████╗  ██║██╔════╝     ██╔════╝██╔══██╗██║╚══██╔══╝██║██╔═══██╗████╗  ██║ 
██║   ██║██║█████╗     ██║       ██║     ██║   ██║██╔██╗ ██║██║  ███╗    █████╗  ██║  ██║██║   ██║   ██║██║   ██║██╔██╗ ██║ 
╚██╗ ██╔╝██║██╔══╝     ██║       ██║     ██║   ██║██║╚██╗██║██║   ██║    ██╔══╝  ██║  ██║██║   ██║   ██║██║   ██║██║╚██╗██║ 
 ╚████╔╝ ██║███████╗   ██║       ╚██████╗╚██████╔╝██║ ╚████║╚██████╔╝    ███████╗██████╔╝██║   ██║   ██║╚██████╔╝██║ ╚████║ 
  ╚═══╝  ╚═╝╚══════╝   ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝     ╚══════╝╚═════╝ ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ 
"""
    subsubtitle = "By Noah Klikauer"
    
    welcome = "Type 's' or 'start' to start the game\nType 'help' for instructions on how to play"
    start = "Round {r} |       Wins: {w}  Deaths: {d}"
    new_round = "New Round (Y/N)? "
    
    current_room = "You are in position {pos}"
    tunnel_connections = "Pathways lead to positions {r0}, {r1}, {r2}"

    action = "!> "
    action_move = "Which position? "
    action_shoot = "Which position? "

    invalid_room = "Invalid position!"
    invalid_action = "Invalid Action!"
    invalid_move = "Can't get there!"
    invalid_shoot = "Can't shoot there!"

    arrows_left = "{count} Bullets Left"
    arrow_miss = "No enemy in position {r}"

    wumpus_nearby = "You hear leaves rustling nearby"
    bat_nearby = "You see one of your tunnels nearby"
    pit_nearby = "Your friends warn you of a trap nearby"

    death = "LOOKS LIKE THE VIET CONG WIN AGAIN"
    win = "YOU KILLED THE VIET CONG SOLDIER!!"

    wumpus_wake = "The Viet Cong solder found you!"
    wumpus_move = "The Viet Cong soldier ran away"
    wumpus_death = "THE VIET CONG SOLDIER SHOT YOU!!"
    pit_enter = "You fell in a trap!"
    bat_enter = "A fellow soldier signals you to climb down into the tunnel"
    no_arrows = "YOU'VE RUN OUT OF BULLETS!"
    
    enable_print = True
    
    @staticmethod
    def print(s, color = "39;49;", end='\n', force = False):
        if not (Lang.enable_print or force): return
        color = color[:len(color)-1]
        print(f"\033[0m\033[{color}m{s}\033[0m", end=end)
    
    
    @staticmethod
    def set_color(color):
        color = color[:len(color)-1]
        print(f"\033[0m\033[{color}m", end="")
        