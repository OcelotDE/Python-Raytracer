"""
Author: 6377468
Project: Python Raytracer for computer graphics
Description: A raytracer that uses multiprocessing to raytrace images in a 3d scene
Date: December 12, 2023
"""

from Hittable.HittableObject import Hittable, HitRecord  # Importing necessary classes
from General.Vectors import dot, Vec3  # Importing dot product function and Vec3 class
from General.Rays import Ray  # Importing Ray class from General.Rays module
from General.Interval import Interval  # Importing Interval class from General.Interval module
from math import fabs  # Importing absolute value function from math module

# A class representing a cube as a hittable object
class Cube(Hittable):
    def __init__(self, min_corner, max_corner, material):
        self.min_corner = min_corner  # Minimum corner of the cube
        self.max_corner = max_corner  # Maximum corner of the cube
        self.material = material  # Material of the cube

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        t_min = ray_t.min  # Initializing t_min with ray's minimum interval value
        t_max = ray_t.max  # Initializing t_max with ray's maximum interval value
        origin = r.origin()  # Ray's origin
        direction = r.direction()  # Ray's direction

        # Loop through x, y, z axes
        for i in range(3):
            inv_d = 1.0 / direction[i]  # Inverse of ray's direction along axis
            t0 = (self.min_corner[i] - origin[i]) * inv_d  # Intersection at min corner along axis
            t1 = (self.max_corner[i] - origin[i]) * inv_d  # Intersection at max corner along axis
            if inv_d < 0.0:
                t0, t1 = t1, t0  # Swap t0 and t1 if inv_d is negative
            t_min = t0 if t0 > t_min else t_min  # Update t_min to maximum of t0 and t_min
            t_max = t1 if t1 < t_max else t_max  # Update t_max to minimum of t1 and t_max
            if t_max <= t_min:
                return False  # No intersection if t_max is less than or equal to t_min

        rec.t = t_min  # Hit distance along the ray
        rec.p = r.at(t_min)  # Point of intersection along the ray
        rec.material = self.material  # Setting hit record material

        # Calculate outward normals based on the hit point's position relative to cube's faces
        outward_normals = [
            Vec3(-1, 0, 0),
            Vec3(1, 0, 0),
            Vec3(0, -1, 0),
            Vec3(0, 1, 0),
            Vec3(0, 0, -1),
            Vec3(0, 0, 1)
        ]
        epsilon = 0.0001  # Small value to handle floating-point imprecision
        for i in range(6):
            # Checking hit point's proximity to cube faces and setting normals accordingly
            if fabs(rec.p[i % 3] - self.min_corner[i % 3]) < epsilon:
                rec.set_face_normal(r, outward_normals[i])
                return True
            elif fabs(rec.p[i % 3] - self.max_corner[i % 3]) < epsilon:
                rec.set_face_normal(r, -outward_normals[i])
                return True

        return False  # No intersection
