"""
Author: 6377468
Project: Python Raytracer for computer graphics
Description: A raytracer that uses multiprocessing to raytrace images in a 3d scene
Date: December 12, 2023
"""

from Hittable.HittableObject import Hittable, HitRecord  # Importing necessary classes
from General.Vectors import dot  # Importing dot product function from General.Vectors module
from General.Rays import Ray  # Importing Ray class from General.Rays module
from General.Interval import Interval  # Importing Interval class from General.Interval module
from math import sqrt  # Importing square root function from math module

# Class representing a sphere as a hittable object
class Sphere(Hittable):
    def __init__(self, center, radius, material):
        self.center = center  # Center of the sphere
        self.radius = radius  # Radius of the sphere
        self.material = material  # Material of the sphere

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        oc = r.origin() - self.center  # Vector from ray origin to sphere center
        a = dot(r.direction(), r.direction())  # Dot product of ray direction with itself (a coefficient)
        b = dot(oc, r.direction())  # Dot product of oc with ray direction (b coefficient)
        c = dot(oc, oc) - self.radius * self.radius  # Square of distance from ray origin to sphere center minus radius
        discriminant = b * b - a * c  # Discriminant of the quadratic equation

        if discriminant > 0:  # If discriminant is positive, calculate the roots
            root = sqrt(discriminant)  # Calculate square root of the discriminant

            # Find the nearest root that lies within the acceptable range
            temp = (-b - root) / a  # Calculate first root
            if not ray_t.surrounds(temp):  # If the root is not within the acceptable range
                temp = (-b + root) / a  # Calculate the other root
                if not ray_t.surrounds(temp):  # If both roots are outside the acceptable range
                    return False  # No intersection

            rec.t = temp  # Set hit record parameter t to the valid root
            rec.p = r.at(rec.t)  # Calculate the hit point using the ray equation
            rec.material = self.material  # Set the hit record's material
            outward_normal = (rec.p - self.center) / self.radius  # Calculate the outward normal
            rec.set_face_normal(r, outward_normal)  # Set the hit record's normal
            return True  # Return intersection

        return False  # No intersection if discriminant is non-positive
