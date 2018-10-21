class Symbol:
    def __init__(self, direction, duration, tollerance=2):
        self.direction = direction
        self.duration = duration
        self.tollerance = tollerance

    def __eq__(self, other):
        if isinstance(other, Symbol):
            if self.direction == other.direction and other.duration - self.tollerance <= self.duration <= other.duration + self.tollerance:
                return True
            else:
                return False

    def __str__(self):
        return "(" + str(self.direction) + " " + str(self.duration) + ")" + " "

    def __lt__(self, other):
        return self.duration < other.duration
