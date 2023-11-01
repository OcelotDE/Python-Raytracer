class Interval:
    def __init__(self, minimum=float('inf'), maximum=float('-inf')):
        self.min = minimum
        self.max = maximum

    def contains(self, x):
        return self.min <= x <= self.max

    def surrounds(self, x):
        return self.min < x < self.max


# Define the empty and universe intervals
empty = Interval(float('inf'), float('-inf'))
universe = Interval(float('-inf'), float('inf'))
