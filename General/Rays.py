from math import sqrt

from General.Vectors import Vec3, dot  # Assuming you have point3 and vec3 classes defined in vec3.py


class Ray:
    def __init__(self, origin=None, direction=None):
        self.orig = origin if origin is not None else Vec3()
        self.dir = direction if direction is not None else Vec3()

    def origin(self):
        return self.orig

    def direction(self):
        return self.dir

    def at(self, t):
        return self.orig + t * self.dir


def hit_sphere(center, radius, r):
    oc = r.origin() - center
    a = dot(r.direction(), r.direction())
    half_b = dot(oc, r.direction())
    c = oc.length_squared() - radius * radius
    discriminant = half_b * half_b - a * c

    if discriminant < 0:
        return -1.0
    else:
        return (-half_b - sqrt(discriminant)) / a


