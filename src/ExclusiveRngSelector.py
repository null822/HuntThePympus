import random

class ExclusiveRngSelector:
    """
    An RNG (random number generator) that ensures the same number is never picked twice
    """
    def __init__(self):
        self.previousValues = []


    def next(self, max: int, min: int = 0):
        """
        Gets the next number in the RNG sequence
        """
        safe = False
        for i in range(min, max + 1):
            if not self.previousValues.__contains__(i):
                safe = True
                break
        if not safe:
            raise Exception("ExclusiveRngSelector has run out of values")
        
        while True:
            value = random.randint(min, max)
            
            if not self.previousValues.__contains__(value):
                self.previousValues.append(value)
                break
        return value