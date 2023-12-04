import math  # Import the math module for mathematical operations
from numpy import random, fabs  # Import specific functions from the numpy library

# Vector class definition
class Vec3:
    # Constructor to initialize a 3D vector
    def __init__(self, e0, e1, e2):
        self.e = (e0, e1, e2)  # Store vector components as a tuple

    # Getter methods for x, y, z components of the vector
    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]

    def z(self):
        return self.e[2]

    # Unary negation of the vector components
    def __neg__(self):
        return Vec3(-self.e[0], -self.e[1], -self.e[2])

    # Indexing operator for accessing vector components
    def __getitem__(self, i):
        return self.e[i]

    # Assignment operator for vector components
    def __setitem__(self, i, value):
        self.e[i] = value

    # Vector subtraction
    def __sub__(self, other):
        return Vec3(self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])

    # Vector addition
    def __add__(self, other):
        return Vec3(self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])

    # In-place vector addition
    def __iadd__(self, other):
        self.e = (self.e[0] + other.e[0], self.e[1] + other.e[1], self.e[2] + other.e[2])
        return self

    # In-place vector subtraction
    def __isub__(self, other):
        self.e = (self.e[0] - other.e[0], self.e[1] - other.e[1], self.e[2] - other.e[2])
        return self

    # Scalar multiplication of a vector
    def __mul__(self, t):
        if isinstance(t, Vec3):
            return Vec3(self.e[0] * t[0], self.e[1] * t[1], self.e[2] * t[2])
        else:
            return Vec3(self.e[0] * t, self.e[1] * t, self.e[2] * t)

    # Right scalar multiplication (same as scalar multiplication)
    def __rmul__(self, t):
        return self * t

    # In-place scalar multiplication
    def __imul__(self, t):
        self.e = (self.e[0] * t, self.e[1] * t, self.e[2] * t)
        return self

    # In-place scalar division
    def __itruediv__(self, t):
        inv_t = 1 / t
        self.e[0] *= inv_t
        self.e[1] *= inv_t
        self.e[2] *= inv_t
        return self

    # Scalar division of a vector
    def __truediv__(self, t):
        return Vec3(self.e[0] / t, self.e[1] / t, self.e[2] / t)

    # Euclidean length of the vector
    def length(self):
        return math.sqrt(self.length_squared())

    # Squared length of the vector
    def length_squared(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    # Check if vector components are near zero
    def near_zero(self):
        s = 1e-8
        return fabs(self.e[0]) < s and fabs(self.e[1]) < s and fabs(self.e[2]) < s

    # Convert vector to string representation
    def __str__(self):
        return f"{self.e[0]} {self.e[1]} {self.e[2]}"

    # Static method to generate a random vector within a range
    @staticmethod
    def random(min: float = 0.0, max: float = 1.0):
        return Vec3(random.uniform(min, max), random.uniform(min, max), random.uniform(min, max))


# Dot product of two vectors
def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


# Cross product of two vectors
def cross(u, v):
    return Vec3(u[1] * v[2] - u[2] * v[1],
                u[2] * v[0] - u[0] * v[2],
                u[0] * v[1] - u[1] * v[0])


# Unit vector from a given vector
def unit_vector(v):
    length = v.length()
    return v / length


# Generate a random point within a unit sphere
def random_in_unit_sphere():
    while True:
        p = Vec3.random(-1, 1)
        if p.length_squared() < 1:
            return p


# Generate a random unit vector
def random_unit_vector():
    return unit_vector(random_in_unit_sphere())


# Generate a random vector on a hemisphere
def random_on_hemisphere(normal: Vec3):
    on_unit_sphere: Vec3 = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere
    else:
        return -on_unit_sphere


# Calculate the reflection of a vector
def reflect(v: Vec3, n: Vec3):
    return v - 2 * dot(v, n) * n


# Calculate the refraction of a vector
def refract(uv, n, etai_over_etat):
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(abs(1.0 - r_out_perp.length_squared())) * n
    return r_out_perp + r_out_parallel
