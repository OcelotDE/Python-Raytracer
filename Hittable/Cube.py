from Hittable.HittableObject import Hittable, HitRecord
from General.Vectors import dot, Vec3
from General.Rays import Ray
from General.Interval import Interval
from math import fabs

class Cube(Hittable):
    def __init__(self, min_corner, max_corner, material):
        self.min_corner = min_corner
        self.max_corner = max_corner
        self.material = material

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        t_min = ray_t.min
        t_max = ray_t.max
        origin = r.origin()
        direction = r.direction()

        for i in range(3):
            inv_d = 1.0 / direction[i]
            t0 = (self.min_corner[i] - origin[i]) * inv_d
            t1 = (self.max_corner[i] - origin[i]) * inv_d
            if inv_d < 0.0:
                t0, t1 = t1, t0
            t_min = t0 if t0 > t_min else t_min
            t_max = t1 if t1 < t_max else t_max
            if t_max <= t_min:
                return False

        rec.t = t_min
        rec.p = r.at(t_min)
        rec.material = self.material

        # Calculate outward normal based on the hit point's position relative to cube's faces
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
            if fabs(rec.p[i % 3] - self.min_corner[i % 3]) < epsilon:
                rec.set_face_normal(r, outward_normals[i])
                return True
            elif fabs(rec.p[i % 3] - self.max_corner[i % 3]) < epsilon:
                rec.set_face_normal(r, -outward_normals[i])
                return True

        return False
