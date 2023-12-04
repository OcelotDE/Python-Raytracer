from General.Vectors import Vec3  # Importing the Vec3 class from General.Vectors module
from numpy import clip, sqrt  # Importing clip function and square root function from numpy

# Function to perform linear to gamma conversion for a single component
def linear_to_gamma(linear_component):
    return sqrt(linear_component)  # Applying square root as the simple gamma approximation

# Function to translate pixel color values to a [0, 255] range for each color component
def write_color(pixel_color, samples_per_pixel):
    # Divide the color components by the number of samples to get the average color
    scale = 1.0 / samples_per_pixel
    r = pixel_color.x() * scale  # Scaling the red component
    g = pixel_color.y() * scale  # Scaling the green component
    b = pixel_color.z() * scale  # Scaling the blue component

    # Apply linear to gamma conversion to the color components
    r = linear_to_gamma(r)  # Applying gamma correction to the red component
    g = linear_to_gamma(g)  # Applying gamma correction to the green component
    b = linear_to_gamma(b)  # Applying gamma correction to the blue component

    # Clamp the color values to [0, 0.999] and map to the [0, 255] range for each color component
    ir = int(256 * clip(r, 0.0, 0.999))  # Clipping and converting red component to integer [0, 255]
    ig = int(256 * clip(g, 0.0, 0.999))  # Clipping and converting green component to integer [0, 255]
    ib = int(256 * clip(b, 0.0, 0.999))  # Clipping and converting blue component to integer [0, 255]

    # Returning a tuple (ir, ig, ib) representing the translated color values for the pixel
    return Vec3(ir, ig, ib).e  # Returning the tuple representation of (ir, ig, ib) for RGB values
