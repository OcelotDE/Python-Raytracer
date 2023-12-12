"""
Author: 6377468
Project: Python Raytracer for computer graphics
Description: A raytracer that uses multiprocessing to raytrace images in a 3d scene
Date: December 12, 2023
"""

from abc import ABC, abstractmethod  # Importing the ABC module and abstractmethod decorator
from General.Vectors import dot  # Importing dot function from General.Vectors module
from General.Interval import Interval  # Importing Interval class from General.Interval module

# Class representing information about a hit on an object
class HitRecord:
    def __init__(self, p=None, normal=None, material=None, t=None, front_face=None):
        self.p = p  # Point of intersection
        self.normal = normal  # Normal vector at the intersection point
        self.material = material  # Material of the object at the intersection
        self.t = t  # Parameter 't' along the ray indicating the distance of the hit
        self.front_face = front_face  # Flag indicating if the hit was on the front face of the object

    def set_face_normal(self, r, outward_normal):
        # Sets the hit record normal vector based on ray direction and outward normal
        self.front_face = dot(r.direction(), outward_normal) < 0  # Checking if the ray direction and normal are facing opposite directions
        self.normal = outward_normal if self.front_face else -outward_normal  # Assigning the normal based on the front face flag

# Abstract class representing a hittable object
class Hittable(ABC):
    @abstractmethod
    def hit(self, r, ray_t: Interval, rec):
        pass  # Abstract method for computing hits on the object
