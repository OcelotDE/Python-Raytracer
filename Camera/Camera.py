import math

import numpy.random as rnd

from General.Interval import Interval
from General.Vectors import Vec3, unit_vector, cross
from Hittable.HittableObject import HitRecord
from General.VectorsColors import write_color
from General.Rays import Ray

from PIL import Image


class Camera:
    # Public stuff
    image_width = 100
    aspect_ratio = 1.0
    samples_per_pixel = 10
    max_depth = 10

    vfov = 90
    lookfrom = Vec3(0, 0, -1)
    lookat = Vec3(0, 0, 0)
    vup = Vec3(0, 1, 0)

    # Private stuff
    __image_height: int
    __camera_center: Vec3
    __pixel00_loc: Vec3
    __pixel_delta_u: Vec3
    __pixel_delta_v: Vec3

    __u: Vec3
    __v: Vec3
    __w: Vec3

    def render(self, world):
        self.__initialize()

        # Create a blank image with RGB mode and white background
        image = Image.new("RGB", (self.image_width, self.__image_height), "white")
        pixels = image.load()

        for j in range(self.__image_height):
            for i in range(self.image_width):
                print(f'rendering frame x={i}/{self.image_width} y={j}/{self.__image_height}')

                self.__calculate_pixel(i, j, world, pixels)



        # Save the image
        image.save("output2.png")

        # Display the image using the default image viewer
        image.show()

    def __initialize(self):
        # TODO: ADD DEFOCUS

        self.__image_height = int(self.image_width / self.aspect_ratio)

        self.__camera_center = self.lookfrom

        # Camera
        focal_length = (self.lookfrom - self.lookat).length()
        theta = math.radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * (self.image_width / self.__image_height)

        # Calculate the u,v,w unit basis vectors for the camera coordinate frame.

        self.__w = unit_vector(self.lookfrom - self.lookat)
        self.__u = unit_vector(cross(self.vup, self.__w))
        self.__v = cross(self.__w, self.__u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges.

        viewport_u = viewport_width * self.__u
        viewport_v = viewport_height * -self.__v

        # Calculate the horizontal and vertical delta vectors from pixel to pixel.

        self.__pixel_delta_u = viewport_u / self.image_width
        self.__pixel_delta_v = viewport_v / self.__image_height

        # Calculate the location of the upper left pixel.
        viewport_upper_left = self.__camera_center - (focal_length * self.__w) - viewport_u / 2 - viewport_v / 2
        self.__pixel00_loc = viewport_upper_left + 0.5 * (self.__pixel_delta_u + self.__pixel_delta_v)

    def __calculate_pixel(self, i, j, world, pixels):
        pixel_color: Vec3 = Vec3(0, 0, 0)
        for sample in range(self.samples_per_pixel):
            r: Ray = self.get_ray(i, j)
            ray_color = self.__ray_color(r, self.max_depth, world)

            pixel_color += ray_color

        # Set pixel color
        write_color(pixels, i, j, pixel_color, self.samples_per_pixel)

    def __ray_color(self, r, depth, world):
        # t = hit_sphere(Vec3(0, 0, -1), 0.5, r)
        # if t > 0.0:
        #    N = unit_vector(r.at(t) - Vec3(0, 0, -1))
        #    return 0.5 * Vec3(N.x() + 1, N.y() + 1, N.z() + 1)

        rec = HitRecord()

        if depth <= 0:
            return Vec3(0, 0, 0)

        if world.hit(r, Interval(0.001, float('inf')), rec):
            scattered, attenuation = rec.material.scatter(r, rec)

            if scattered and attenuation:
                color = self.__ray_color(scattered, depth - 1, world)
                return attenuation * color

            return Vec3(0, 0, 0)

        unit_direction = unit_vector(r.direction())
        a = 0.5 * (unit_direction.y() + 1.0)
        white_color = Vec3(1.0, 1.0, 1.0)
        blue_color = Vec3(0.5, 0.7, 1.0)
        blended_color = (1.0 - a) * white_color + a * blue_color
        return blended_color

    def get_ray(self, i, j):
        # Get a randomly sampled camera ray for the pixel at location i, j.

        pixel_center = self.__pixel00_loc + (i * self.__pixel_delta_u) + (j * self.__pixel_delta_v)
        pixel_sample = pixel_center + self.__pixel_sample_square()

        ray_origin = self.__camera_center
        ray_direction = pixel_sample - ray_origin

        return Ray(ray_origin, ray_direction)

    def __pixel_sample_square(self):
        # Returns a random point in the square surrounding a pixel at the origin.
        px = -0.5 + rnd.random()
        py = -0.5 + rnd.random()
        return self.__pixel_delta_u * px + self.__pixel_delta_v * py
