from Hittable.HittableObject import Hittable, HitRecord  # Importing necessary classes
from General.Rays import Ray  # Importing Ray class from General.Rays module
from General.Vectors import Vec3  # Importing Vec3 class from General.Vectors module
from General.Interval import Interval  # Importing Interval class from General.Interval module

# A class representing a list of hittable objects
class HittableList(Hittable):
    def __init__(self):
        self.objects = []  # Initializing an empty list to store hittable objects

    def clear(self):
        self.objects.clear()  # Clearing the list of hittable objects

    def add(self, added_hittable: Hittable):
        self.objects.append(added_hittable)  # Adding a hittable object to the list

    def hit(self, r: Ray, ray_t: Interval, rec: HitRecord) -> bool:
        # Temporary record to store hit information
        temp_rec = HitRecord(Vec3(0, 0, 0), Vec3(0, 0, 0), 0, False)

        # Initialize variables for hit detection
        hit_anything = False
        closest_so_far = ray_t.max

        # Iterate through all objects in the list
        for obj in self.objects:
            # Check for intersection with the current object
            if obj.hit(r, Interval(ray_t.min, closest_so_far), temp_rec):
                hit_anything = True  # An object has been hit
                closest_so_far = temp_rec.t  # Update the closest hit so far
                # Copy hit record information to the provided hit record
                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.front_face = temp_rec.front_face
                rec.material = temp_rec.material

        return hit_anything  # Return whether anything was hit in the list
