from General.Vectors import Vec3
from Hittable.HittableList import HittableList
from Hittable.Sphere import Sphere
from Hittable.Cube import Cube
from Camera.Camera import Camera
from Material import Lambertian, Metal, Dielectric

from numpy.random import random as random_float
from numpy.random import uniform


if __name__ == "__main__":
    # Generate world and add elements into it
    world = HittableList()

    material_ground = Lambertian(Vec3(0.5, 0.5, 0.5))
    material_center = Lambertian(Vec3(0.7, 0.5, 1.0))
    material_brushed_metal = Metal(Vec3(0.8, 0.8, 0.8), 0.3)
    material_gold = Metal(Vec3(0.8, 0.6, 0.2), 0.0)
    material_pink = Metal(Vec3(0.7, 0.0, 0.3), 0.1)
    material_glass = Dielectric(1.5)

    world.add(Sphere(Vec3(0, -1000, 0), 1000, material_ground))

    # for a in range(-11, 11):
    #     for b in range(-11, 11):
    #         choose_mat = random_float()
    #         center = Vec3(a + 0.9 * random_float(), 0.2, b + 0.9 * random_float())
    #         if (center - Vec3(4, 0.2, 0)).length() > 0.9:
    #             if choose_mat < 0.8:
    #                 # Lambertian material (diffuse)
    #                 albedo = Vec3.random() * Vec3.random()
    #                 sphere_material = Lambertian(albedo)
    #             elif choose_mat < 0.95:
    #                 # Metal material
    #                 albedo = Vec3.random(0.5, 1)
    #                 fuzz = uniform(0, 0.5)
    #                 sphere_material = Metal(albedo, fuzz)
    #             else:
    #                 # Dielectric material (glass)
    #                 sphere_material = Dielectric(1.5)
    #             world.add(Sphere(center, 0.2, sphere_material))

    world.add(Cube(Vec3(-3, 0, -5), Vec3(-1, 2, -3), material_pink))
    world.add(Cube(Vec3(0, 0, -5), Vec3(1, 1, -4), material_gold))

    world.add(Sphere(Vec3(1, 1, 2), 1.0, material_glass))

    world.add(Sphere(Vec3(-4, 1, 0), 1.0, material_brushed_metal))

    world.add(Sphere(Vec3(4, 0.5, 1), 0.5, material_gold))

    # Create camera and render the world
    cam = Camera()
    #cam.aspect_ratio = 16.0 / 9.0 # removed due to a bug
    cam.image_width = 400
    cam.samples_per_pixel = 100
    cam.max_depth = 50
    cam.vfov = 31
    cam.lookfrom = Vec3(13, 3, 5)
    cam.lookat = Vec3(0, 0, 0)
    cam.vup = Vec3(0, 1, 0)
    cam.render(world)
