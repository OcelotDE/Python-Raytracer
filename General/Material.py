from abc import ABC, abstractmethod  # Imports the ABC module and abstractmethod decorator
from General.Rays import Ray  # Imports the Ray class from General.Rays module
from General.Vectors import Vec3, random_unit_vector, reflect, unit_vector, \
    dot  # Imports specific functions/classes from General.Vectors module
from Hittable.HittableObject import HitRecord  # Imports the HitRecord class from Hittable.HittableObject module

from math import sqrt  # Imports the sqrt function from the math module


# Defines a Material abstract base class with a required scatter method
class Material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord) -> (Ray, Vec3):
        pass


# Defines a Lambertian material class inheriting from Material
class Lambertian(Material):
    # Initializes the Lambertian material with a specified albedo
    def __init__(self, albedo: Vec3):
        self.albedo = albedo

    # Implements the scatter method for Lambertian materials
    def scatter(self, r_in: Ray, rec: HitRecord) -> (Ray, Vec3):
        # Calculates scattered direction for Lambertian materials
        scatter_direction: Vec3 = rec.normal + random_unit_vector()

        # Handles cases where the scatter direction is close to zero
        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        # Creates a scattered Ray and sets attenuation for Lambertian materials
        scattered = Ray(rec.p, scatter_direction)  # Creates a scattered Ray
        attenuation = self.albedo  # Sets attenuation for Lambertian materials
        return scattered, attenuation


# Defines a Metal material class inheriting from Material
class Metal(Material):
    # Initializes the Metal material with specified albedo and fuzziness
    def __init__(self, albedo: Vec3, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1  # Clamps fuzziness to 1

    # Implements the scatter method for Metal materials
    def scatter(self, r_in, rec) -> (Ray, Vec3):
        # Calculates reflected direction for Metal materials
        reflected: Vec3 = reflect(unit_vector(r_in.direction()), rec.normal)

        # Calculates scattered Ray with some fuzziness for Metal materials
        scattered = Ray(rec.p, reflected + self.fuzz * random_unit_vector())  # Adds fuzziness to the reflected direction
        attenuation = self.albedo  # Sets attenuation for Metal materials
        return scattered, attenuation


# Defines a Dielectric material class inheriting from Material
class Dielectric(Material):
    # Initializes the Dielectric material with a specified index of refraction
    def __init__(self, index_of_refraction):
        self.ir = index_of_refraction

    # Implements the scatter method for Dielectric materials
    def scatter(self, r_in: Ray, rec: HitRecord) -> (Ray, Vec3):
        # Sets initial attenuation for Dielectric materials
        attenuation = Vec3(1.0, 1.0, 1.0)

        # Calculates refraction ratios and directions for Dielectric materials
        refraction_ratio = 1.0 / self.ir if rec.front_face else self.ir
        unit_direction = unit_vector(r_in.direction())  # Calculates unit direction of the ray
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)  # Calculates cosine of the angle between the ray and normal
        sin_theta = sqrt(1.0 - cos_theta * cos_theta)  # Calculates sine of the angle between the ray and normal
        cannot_refract = refraction_ratio * sin_theta > 1.0  # Checks if the ray cannot be refracted
        direction = reflect(unit_direction, rec.normal) if cannot_refract else self.refract(unit_direction, rec.normal,
                                                                                            refraction_ratio)

        # Creates a scattered Ray for Dielectric materials
        scattered = Ray(rec.p, direction)
        return scattered, attenuation

    # Defines a static method to calculate refraction for Dielectric materials
    @staticmethod
    def refract(uv, n, etai_over_etat):
        cos_theta = min(dot(-uv, n), 1.0)  # Calculates cosine of the angle between the ray and normal
        r_out_perp = etai_over_etat * (uv + cos_theta * n)  # Calculates perpendicular component of the refracted ray
        r_out_parallel = -sqrt(abs(1.0 - r_out_perp.length_squared())) * n  # Calculates parallel component of the refracted ray
        return r_out_perp + r_out_parallel  # Returns the refracted ray


# Defines a DiffuseLight material class inheriting from Material
class DiffuseLight(Material):
    # Initializes the DiffuseLight material with specified emission and scale factor
    def __init__(self, emit: Vec3, scale_factor: float = 1.0):
        self.emit = emit * scale_factor  # Sets the emission for the material

    # Implements the scatter method for DiffuseLight materials
    def scatter(self, r_in: Ray, rec: HitRecord) -> (Ray, Vec3):
        # Light-emitting materials do not scatter, so returns None for the scattered ray
        return None, self.emit
