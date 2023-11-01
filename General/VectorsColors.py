from General.Vectors import Vec3
from numpy import clip, sqrt


def linear_to_gamma(linear_component):
    return sqrt(linear_component)


def write_color(pixels, x, y, pixel_color, samples_per_pixel):
    # Divide the color by the number of samples.
    scale = 1.0 / samples_per_pixel
    r = pixel_color.x() * scale
    g = pixel_color.y() * scale
    b = pixel_color.z() * scale

    # Apply the linear to gamma transform
    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)

    # Clamp the color values to [0, 0.999] and write the translated [0,255] value of each color component.
    ir = int(256 * clip(r, 0.0, 0.999))
    ig = int(256 * clip(g, 0.0, 0.999))
    ib = int(256 * clip(b, 0.0, 0.999))

    pixels[x, y] = Vec3(ir, ig, ib).e
