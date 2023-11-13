import math

import numpy.random as rnd

from General.Interval import Interval
from General.Vectors import Vec3, unit_vector, cross
from Hittable.HittableObject import HitRecord
from General.VectorsColors import write_color
from General.Rays import Ray

from PIL import Image

import datetime

import multiprocessing
import numpy as np

progress: int = 0


def render_chunk(args):
    chunk_start, chunk_end, camera, world = args
    local_results = []
    for j in range(chunk_start, chunk_end):
        for i in range(camera.image_width):
            pixel_color = Vec3(0, 0, 0)
            for sample in range(camera.samples_per_pixel):
                r = camera.get_ray(i, j)
                ray_color = camera._Camera__ray_color(r, camera.max_depth, world)
                pixel_color += ray_color
            color_value = write_color(pixel_color, camera.samples_per_pixel)
            local_results.append(color_value)
    return local_results


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

        # Number of CPU cores to utilize
        num_cores = multiprocessing.cpu_count()

        # Divide the image into chunks for parallel processing
        chunk_size = self.image_width // num_cores

        # Combine local results into the final image data
        final_image_data = []

        # Create a pool of workers
        with multiprocessing.Pool(processes=num_cores) as pool:
            # Use imap to asynchronously process chunks and get results
            chunk_results = pool.imap(render_chunk, [(i * chunk_size, (i + 1) * chunk_size, self, world) for i in
                                                     range(num_cores)])

            # Track processed chunks for progress indication
            processed_chunks = 0

            # Iterate through chunk results as they become available
            for local_results in chunk_results:
                processed_chunks += 1
                print(f"Processed {processed_chunks} out of {num_cores} chunks")

                # Combine local results into the final image data
                final_image_data.extend(local_results)

        real_size = np.square(self.image_width) * 3
        current_size = np.array(final_image_data).size
        difference = real_size - current_size

        print(f"real size is {real_size}")
        print(f"got {current_size}")
        print(f"difference is {difference}")
        if current_size < real_size:  # prevent generation error due to rounding during divisions
            last_color_value = final_image_data[len(final_image_data) - 1]
            for i in range(int(difference / 3)):
                final_image_data.append(last_color_value)  # fill array up with last pixel of image

        print(f"adjusted to {np.array(final_image_data).size}")

        # Create a NumPy array from the combined results
        image_array = np.array(final_image_data, dtype=np.uint8).reshape(
            (self.image_width, self.image_width, 3))

        # Create an image from the NumPy array
        image = Image.fromarray(image_array, 'RGB')

        # Save the image
        image.save(f"outputs/output-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")

        # Display the image using the default image viewer
        image.show()

    def __initialize(self):

        self.__image_height = self.image_width

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

    def __ray_color(self, r, depth, world):
        if depth <= 0:
            return Vec3(0, 0, 0)  # Return black for rays that exceed recursion depth

        rec = HitRecord()

        if world.hit(r, Interval(0.001, float('inf')), rec):
            emitted = rec.material.emit if hasattr(rec.material, 'emit') else None

            if emitted is not None:
                return emitted  # If the material emits light, return the emitted color

            scattered, attenuation = rec.material.scatter(r, rec)
            if scattered is not None:
                return attenuation * self.__ray_color(scattered, depth - 1, world)

        unit_direction = unit_vector(r.direction())
        t = 0.5 * (unit_direction.y() + 1.0)
        return (1.0 - t) * Vec3(1.0, 1.0, 1.0) + t * Vec3(0.5, 0.7, 1.0)

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
