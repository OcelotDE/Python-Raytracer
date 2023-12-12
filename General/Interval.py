"""
Author: 6377468
Project: Python Raytracer for computer graphics
Description: A raytracer that uses multiprocessing to raytrace images in a 3d scene
Date: December 12, 2023
"""

# Class representing an interval defined by a minimum and maximum value
class Interval:
    def __init__(self, minimum=float('inf'), maximum=float('-inf')):
        self.min = minimum  # Initializing the minimum value of the interval
        self.max = maximum  # Initializing the maximum value of the interval

    # Check if a value x is within the interval
    def contains(self, x):
        return self.min <= x <= self.max  # Returns True if x is within the interval, False otherwise

    # Check if a value x is strictly within the interval
    def surrounds(self, x):
        return self.min < x < self.max  # Returns True if x is strictly within the interval, False otherwise

# Define two special intervals: an empty interval and a universe interval
empty = Interval(float('inf'), float('-inf'))  # Represents an empty interval where min > max initially
universe = Interval(float('-inf'), float('inf'))  # Represents a universe interval that spans from negative infinity to positive infinity
