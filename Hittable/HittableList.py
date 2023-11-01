from Hittable.HittableObject import Hittable, HitRecord
from General.Rays import Ray
from General.Vectors import Vec3
from General.Interval import Interval


class HittableList(Hittable):
    def __init__(self):
        self.objects = []

    def clear(self):
        self.objects.clear()

    def add(self, added_hittable: Hittable):
        self.objects.append(added_hittable)

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        temp_rec = HitRecord(Vec3(0, 0, 0), Vec3(0, 0, 0), 0, False)
        hit_anything = False
        closest_so_far = ray_t.max

        for object in self.objects:
            if object.hit(r, Interval(ray_t.min, closest_so_far), temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.front_face = temp_rec.front_face
                rec.material = temp_rec.material

        return hit_anything
