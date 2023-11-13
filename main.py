import numpy as np

from General.Vectors import Vec3
from Hittable.HittableList import HittableList
from Hittable.Sphere import Sphere
from Hittable.Cube import Cube
from Camera.Camera import Camera
from Material import Lambertian, Metal, Dielectric, DiffuseLight

import time

if __name__ == "__main__":
    # Generate world and add elements into it
    world = HittableList()

    material_ground = Lambertian(Vec3(0.5, 0.5, 0.5))
    material_center = Lambertian(Vec3(0.7, 0.5, 1.0))
    material_brushed_metal = Metal(Vec3(0.8, 0.8, 0.8), 0.3)
    material_gold = Metal(Vec3(0.8, 0.6, 0.2), 0.0)
    material_pink = Metal(Vec3(0.7, 0.0, 0.3), 0.1)
    material_glass = Dielectric(1.5)
    material_light = DiffuseLight(Vec3(0, 0, 1), 40.0)

    world.add(Sphere(Vec3(0, -1000, 0), 1000, material_ground))

    # for a in range(-11, 11, 3):
    #     for b in range(-11, 11, 3):
    #         choose_mat = random_float()
    #         center = Vec3(a + 0.9 * random_float(), 0.2, b + 0.9 * random_float())
    #         if (center - Vec3(4, 0.2, 0)).length() > 0.9:
    #             if choose_mat < 0.7:
    #                 # Lambertian material (diffuse)
    #                 albedo = Vec3.random() * Vec3.random()
    #                 sphere_material = Lambertian(albedo)
    #             elif choose_mat < 0.80:
    #                 # Metal material
    #                 albedo = Vec3.random(0.5, 1)
    #                 fuzz = uniform(0, 0.5)
    #                 sphere_material = Metal(albedo, fuzz)
    #             elif choose_mat < 0.95:
    #                 sphere_material = DiffuseLight(Vec3(random_float(), random_float(), random_float()), random_float() * 3.0)
    #             else:
    #                 # Dielectric material (glass)
    #                 sphere_material = Dielectric(1.5)
    #             world.add(Sphere(center, 0.2, sphere_material))

    world.add(Cube(Vec3(-3, 0, -5), Vec3(-1, 2, -3), material_pink))
    world.add(Cube(Vec3(0, 0, -5), Vec3(1, 1, -4), material_light))

    world.add(Sphere(Vec3(1, 1, 2), 1.0, material_glass))

    world.add(Sphere(Vec3(-4, 1, 0), 1.0, material_brushed_metal))

    world.add(Sphere(Vec3(4, 0.5, 1), 0.5, material_gold))

    # Create camera and render the world
    cam = Camera()
    cam.image_width = 500
    cam.samples_per_pixel = 10
    cam.max_depth = 10
    cam.vfov = 31
    cam.lookfrom = Vec3(13, 3, 5)
    cam.lookat = Vec3(0, 0, 0)
    cam.vup = Vec3(0, 1, 0)

    start_time = time.time()

    cam.render(world)

    print(f"Render finished after {int(time.time() - start_time)} seconds.")
