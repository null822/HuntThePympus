import random

class ExclusiveRngSelector:
    previousValues = []
    
    def next(self, max: int, min: int = 0):
        while True:
            value = random.randint(min, max)
            if not self.previousValues.__contains__(value):
                self.previousValues.append(value)
                break
        return value