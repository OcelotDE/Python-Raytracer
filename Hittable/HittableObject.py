from abc import ABC, abstractmethod
from General.Vectors import dot
from General.Interval import Interval


class HitRecord:
    def __init__(self, p=None, normal=None, material=None, t=None, front_face=None):
        self.p = p
        self.normal = normal
        self.material = material
        self.t = t
        self.front_face = front_face

    def set_face_normal(self, r, outward_normal):
        # Sets the hit record normal vector.
        # NOTE: the parameter `outward_normal` is assumed to have unit length.

        self.front_face = dot(r.direction(), outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable(ABC):
    @abstractmethod
    def hit(self, r, ray_t: Interval, rec):
        pass
