
class ActionResult:
    """
    In a competent programming language, this would be an enum representing what happened after an action was executed.
    """
    success = 0
    """
    The action succeeded
    """
    fail = 1
    """
    The action failed
    """
    win = 2
    """
    The player won the game
    """
    death = 3
    """
    The player lost the game
    """
    restartRound = 4
    """
    The current round should be restarted completely, including all messages printed at the start
    """