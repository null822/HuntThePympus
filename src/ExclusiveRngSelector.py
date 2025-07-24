import random

class ExclusiveRngSelector:
    """
    An RNG (random number generator) that ensures the same number is never picked twice
    """
    previousValues = []

    
    def next(self, max: int, min: int = 0):
        """
        Gets the next number in the RNG sequence
        """
        while True:
            value = random.randint(min, max)
            if not self.previousValues.__contains__(value):
                self.previousValues.append(value)
                break
        return value