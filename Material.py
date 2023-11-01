from abc import ABC, abstractmethod
from General.Rays import Ray
from General.Vectors import Vec3, random_unit_vector, reflect, unit_vector, dot
from Hittable.HittableObject import HitRecord

from math import sqrt


class Material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec: HitRecord) -> (Ray, Vec3):
        pass


class Lambertian(Material):
    def __init__(self, albedo: Vec3):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> (Ray, Vec3):
        scatter_direction: Vec3 = rec.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return scattered, attenuation


class Metal(Material):
    def __init__(self, albedo: Vec3, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, r_in, rec) -> (Ray, Vec3):
        reflected: Vec3 = reflect(unit_vector(r_in.direction()), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * random_unit_vector())
        attenuation = self.albedo
        return scattered, attenuation


class Dielectric(Material):
    def __init__(self, index_of_refraction):
        self.ir = index_of_refraction

    def scatter(self, r_in: Ray, rec: HitRecord) -> (Ray, Vec3):
        attenuation = Vec3(1.0, 1.0, 1.0)
        refraction_ratio = 1.0 / self.ir if rec.front_face else self.ir

        unit_direction = unit_vector(r_in.direction())
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = sqrt(1.0 - cos_theta * cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0
        direction = reflect(unit_direction, rec.normal) if cannot_refract else self.refract(unit_direction, rec.normal,
                                                                                            refraction_ratio)

        scattered = Ray(rec.p, direction)
        return scattered, attenuation

    @staticmethod
    def refract(uv, n, etai_over_etat):
        cos_theta = min(dot(-uv, n), 1.0)
        r_out_perp = etai_over_etat * (uv + cos_theta * n)
        r_out_parallel = -sqrt(abs(1.0 - r_out_perp.length_squared())) * n
        return r_out_perp + r_out_parallel
