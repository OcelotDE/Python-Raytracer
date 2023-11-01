import math
from numpy import random, fabs


class Vec3:
    def __init__(self, e0, e1, e2):
        self.e = (e0, e1, e2)

    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]

    def z(self):
        return self.e[2]

    def __neg__(self):
        return Vec3(-self.e[0], -self.e[1], -self.e[2])

    def __getitem__(self, i):
        return self.e[i]

    def __setitem__(self, i, value):
        self.e[i] = value

    def __sub__(self, other):
        return Vec3(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])

    def __add__(self, other):
        return Vec3(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])

    def __iadd__(self, other):
        self.e = (self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])
        return self

    def __isub__(self, other):
        self.e = (self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])
        return self

    def __mul__(self, t):
        if isinstance(t, Vec3):
            return Vec3(self.e[0] * t[0], self.e[1] * t[1], self.e[2] * t[2])
        else:
            return Vec3(self.e[0] * t, self.e[1] * t, self.e[2] * t)

    def __rmul__(self, t):
        return self * t

    def __imul__(self, t):
        self.e = (self.e[0] * t, self.e[1] * t, self.e[2] * t)
        return self

    def __itruediv__(self, t):
        inv_t = 1 / t
        self.e[0] *= inv_t
        self.e[1] *= inv_t
        self.e[2] *= inv_t
        return self

    def __truediv__(self, t):
        return Vec3(self.e[0] / t, self.e[1] / t, self.e[2] / t)

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    def near_zero(self):
        s = 1e-8
        return fabs(self.e[0]) < s and fabs(self.e[1]) < s  and fabs(self.e[2]) < s

    def __str__(self):
        return f"{self.e[0]} {self.e[1]} {self.e[2]}"

    @staticmethod
    def random(min: float = 0.0, max: float = 1.0):
        return Vec3(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def cross(u, v):
    return Vec3(u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0])


def unit_vector(v):
    length = v.length()
    return v / length


def random_in_unit_sphere():
    while True:
        p = Vec3.random(-1, 1)
        if p.length_squared() < 1:
            return p


def random_unit_vector():
    return unit_vector(random_in_unit_sphere())


def random_on_hemisphere(normal: Vec3):
    on_unit_sphere: Vec3 = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere
    else:
        return -on_unit_sphere


def reflect(v: Vec3, n: Vec3):
    return v - 2 * dot(v, n) * n


def refract(uv, n, etai_over_etat):
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
    return r_out_perp + r_out_parallel
