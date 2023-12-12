"""
Author: 6377468
Project: Python Raytracer for computer graphics
Description: A raytracer that uses multiprocessing to raytrace images in a 3d scene
Date: December 12, 2023
"""

# Imported libraries
import math  # Import the math module for mathematical operations
import numpy.random as rnd  # Import a subset of the numpy library for random number generation
from General.Interval import Interval  # Import Interval class from General.Interval module
from General.Vectors import Vec3, unit_vector, cross  # Import Vec3, unit_vector, and cross functions from General.Vectors module
from Hittable.HittableObject import HitRecord  # Import HitRecord class from Hittable.HittableObject module
from General.VectorsColors import write_color  # Import write_color function from General.VectorsColors module
from General.Rays import Ray  # Import Ray class from General.Rays module
from PIL import Image  # Import Image class from PIL library for image processing
import datetime  # Import datetime module for working with dates and times
import multiprocessing  # Import multiprocessing module for parallel processing
import numpy as np  # Import numpy library for numerical operations

# Global variable to track progress
progress: int = 0

# Function to render a chunk of the scene in parallel
def render_chunk(args):
    # Args: start chunk, end chunk, camera, world
    chunk_start, chunk_end, camera, world = args  # Unpack arguments
    local_results = []  # Initialize a list to store local results
    for j in range(chunk_start, chunk_end):  # Iterate through rows in the chunk
        for i in range(camera.image_width):  # Iterate through columns in the image
            pixel_color = Vec3(0, 0, 0)  # Initialize pixel color to black
            for sample in range(camera.samples_per_pixel):  # Perform multiple samples per pixel
                r = camera.get_ray(i, j)  # Get a ray for the pixel
                ray_color = camera._Camera__ray_color(r, camera.max_depth, world)  # Get color for the ray
                pixel_color += ray_color  # Accumulate ray colors for the pixel
            color_value = write_color(pixel_color, camera.samples_per_pixel)  # Calculate final color value
            local_results.append(color_value)  # Store color value in local results
    return local_results  # Return local results for the chunk

# Camera class definition
class Camera:
    # Public attributes defining rendering settings
    image_width = 100  # Width of the rendered image
    aspect_ratio = 1.0  # Aspect ratio of the image
    samples_per_pixel = 10  # Number of samples per pixel for anti-aliasing
    max_depth = 10  # Maximum depth for ray recursion
    vfov = 90  # Vertical field of view
    lookfrom = Vec3(0, 0, -1)  # Camera's look-from position
    lookat = Vec3(0, 0, 0)  # Camera's look-at position
    vup = Vec3(0, 1, 0)  # Camera's up vector

    # Private attributes for internal calculations
    __image_height: int  # Height of the image
    __camera_center: Vec3  # Camera center position
    __pixel00_loc: Vec3  # Location of the top-left pixel
    __pixel_delta_u: Vec3  # Pixel-to-pixel change in the horizontal direction
    __pixel_delta_v: Vec3  # Pixel-to-pixel change in the vertical direction
    __u: Vec3  # Horizontal unit vector
    __v: Vec3  # Vertical unit vector
    __w: Vec3  # Directional unit vector

    # Function to render the scene
    def render(self, world):
        self.__initialize()  # Initialize camera parameters

        # Number of CPU cores available for parallel processing
        num_cores = multiprocessing.cpu_count()

        # Divide the image into chunks for parallel processing
        chunk_size = self.image_width // num_cores

        # Combine local results into the final image data
        final_image_data = []

        # Create a pool of workers for parallel processing
        with multiprocessing.Pool(processes=num_cores) as pool:
            # Use imap to asynchronously process chunks and gather results
            chunk_results = pool.imap(render_chunk, [(i * chunk_size, (i + 1) * chunk_size, self, world) for i in range(num_cores)])

            # Track processed chunks for progress indication
            processed_chunks = 0

            # Iterate through chunk results as they become available
            for local_results in chunk_results:
                processed_chunks += 1
                print(f"Processed {processed_chunks} out of {num_cores} chunks")  # Print progress information

                # Combine local results into the final image data
                final_image_data.extend(local_results)  # Extend the final image data with local results

        # Calculate expected and actual size of the final image data
        real_size = np.square(self.image_width) * 3
        current_size = np.array(final_image_data).size
        difference = real_size - current_size

        print(f"real size is {real_size}")  # Print information about the expected size
        print(f"got {current_size}")  # Print information about the actual size
        print(f"difference is {difference}")  # Print the difference in size

        # Check and adjust the final image data size to prevent generation errors
        if current_size < real_size:
            last_color_value = final_image_data[len(final_image_data) - 1]
            for i in range(int(difference / 3)):
                final_image_data.append(last_color_value)  # Fill array up with the last pixel of the image

        print(f"adjusted to {np.array(final_image_data).size}")  # Print adjusted size information

        # Create a NumPy array from the combined results
        image_array = np.array(final_image_data, dtype=np.uint8).reshape((self.image_width, self.image_width, 3))

        # Create an image from the NumPy array
        image = Image.fromarray(image_array, 'RGB')

        # Save the image with a timestamp in the filename
        image.save(f"outputs/output-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png")

        # Display the image using the default image viewer
        image.show()

    # Function to initialize camera parameters
    def __initialize(self):
        # Set the image height equal to the image width
        self.__image_height = self.image_width

        # Set the camera center to the look-from position
        self.__camera_center = self.lookfrom

        # Calculate camera parameters based on the settings
        focal_length = (self.lookfrom - self.lookat).length()
        theta = math.radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * (self.image_width / self.__image_height)
        self.__w = unit_vector(self.lookfrom - self.lookat)
        self.__u = unit_vector(cross(self.vup, self.__w))
        self.__v = cross(self.__w, self.__u)
        viewport_u = viewport_width * self.__u
        viewport_v = viewport_height * -self.__v
        self.__pixel_delta_u = viewport_u / self.image_width
        self.__pixel_delta_v = viewport_v / self.__image_height
        viewport_upper_left = self.__camera_center - (focal_length * self.__w) - viewport_u / 2 - viewport_v / 2
        self.__pixel00_loc = viewport_upper_left + 0.5 * (self.__pixel_delta_u + self.__pixel_delta_v)

    # Function to calculate the color of a ray recursively
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

    # Function to get a ray for a given pixel location
    def get_ray(self, i, j):
        pixel_center = self.__pixel00_loc + (i * self.__pixel_delta_u) + (j * self.__pixel_delta_v)
        pixel_sample = pixel_center + self.__pixel_sample_square()
        ray_origin = self.__camera_center
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    # Function to generate a random point in a square around a pixel
    def __pixel_sample_square(self):
        px = -0.5 + rnd.random()
        py = -0.5 + rnd.random()
        return self.__pixel_delta_u * px + self.__pixel_delta_v * py
