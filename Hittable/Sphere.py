from Hittable.HittableObject import Hittable, HitRecord
from General.Vectors import dot
from General.Rays import Ray
from General.Interval import Interval
from math import sqrt


class Sphere(Hittable):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        oc = r.origin() - self.center
        a = dot(r.direction(), r.direction())
        b = dot(oc, r.direction())
        c = dot(oc, oc) - self.radius * self.radius
        discriminant = b * b - a * c

        if discriminant > 0:
            root = sqrt(discriminant)

            # Find the nearest root that lies in the acceptable range.
            temp = (-b - root) / a
            if not ray_t.surrounds(temp):
                temp = (-b + root) / a
                if not ray_t.surrounds(temp):
                    return False

            rec.t = temp
            rec.p = r.at(rec.t)
            rec.material = self.material
            outward_normal = (rec.p - self.center) / self.radius
            rec.set_face_normal(r, outward_normal)
            return True

        return False
