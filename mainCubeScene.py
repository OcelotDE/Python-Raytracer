from General.Vectors import Vec3
from Hittable.HittableList import HittableList
from Hittable.Sphere import Sphere
from Hittable.Cube import Cube
from Camera.Camera import Camera
from General.Material import Lambertian, DiffuseLight

import time

if __name__ == "__main__":
    # Generate world and add elements into it
    world = HittableList()

    wall1 = Lambertian(Vec3(1, 0.5, 0.5))
    wall2 = ceiling = floor = Lambertian(Vec3(0.5, 0.5, 0.5))
    wall3 = Lambertian(Vec3(0.51, 0.5, 0.1))


    world.add(Cube(Vec3(-10, -1, -10), Vec3(10, 0, 10), floor))
    world.add(Cube(Vec3(-10, 10, -10), Vec3(10, 11, 10), ceiling))


    world.add(Cube(Vec3(0, 0, 10), Vec3(10, 10, 11), wall1))
    world.add(Cube(Vec3(0, 0, -10), Vec3(10, 10, -9), wall3))
    world.add(Cube(Vec3(0, 0, -10), Vec3(1, 10, 10), wall2))
    #world.add(Cube(Vec3(0, 0, -5), Vec3(1, 1, -4), material_light))



    material_light = DiffuseLight(Vec3(1, 1, 1), 8.0)


    world.add(Sphere(Vec3(0, 10, 0), 2.0, material_light))

    # Create camera and render the world
    cam = Camera()
    cam.image_width = 400
    cam.samples_per_pixel = 200
    cam.max_depth = 10
    cam.vfov = 140
    cam.lookfrom = Vec3(10, 5, 0)
    cam.lookat = Vec3(0, 4, 0)
    cam.vup = Vec3(0, 1, 0)

    start_time = time.time()

    cam.render(world)

    print(f"Render finished after {int(time.time() - start_time)} seconds.")
