"""
Author: 6377468
Project: Python Raytracer for computer graphics
Description: A raytracer that uses multiprocessing to raytrace images in a 3d scene
Date: December 12, 2023
"""

from math import sqrt  # Import the square root function from the math module
from General.Vectors import Vec3, dot  # Import Vec3 class and dot function from General.Vectors module

# Ray class definition
class Ray:
    # Constructor to initialize a ray with origin and direction
    def __init__(self, origin=None, direction=None):
        self.orig = origin if origin is not None else Vec3()  # Set origin to provided value or default Vec3(0, 0, 0)
        self.dir = direction if direction is not None else Vec3()  # Set direction to provided value or default Vec3(0, 0, 0)

    # Getter method for ray origin
    def origin(self):
        return self.orig

    # Getter method for ray direction
    def direction(self):
        return self.dir

    # Calculate a point along the ray at parameter t
    def at(self, t):
        return self.orig + t * self.dir  # Calculate point using ray equation P(t) = O + tD


# Function to calculate ray-sphere intersection
def hit_sphere(center, radius, r):
    oc = r.origin() - center  # Vector from ray origin to sphere center
    a = dot(r.direction(), r.direction())  # Dot product of ray direction with itself (a coefficient)
    half_b = dot(oc, r.direction())  # Dot product of oc with ray direction (b coefficient)
    c = oc.length_squared() - radius * radius  # Square of distance from ray origin to sphere center minus radius
    discriminant = half_b * half_b - a * c  # Discriminant of the quadratic equation

    if discriminant < 0:  # If discriminant is negative, no real roots, no intersection
        return -1.0
    else:  # If discriminant is non-negative, calculate and return the nearest intersection point
        return (-half_b - sqrt(discriminant)) / a  # Calculate t parameter for intersection point
