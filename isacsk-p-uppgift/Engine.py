def dot_product(vector_1, vector_2):
    """Defines the dot-product of two threedimensional vectors."""
    product = vector_1[0]*vector_2[0] + vector_1[1]*vector_2[1] + vector_1[2]*vector_2[2]
    return product


def vector_addition(vector_1, vector_2):
    """Defines addition of two threedimensional vectors."""
    vector_sum = (vector_1[0]+vector_2[0], vector_1[1]+vector_2[1], vector_1[2]+vector_2[2])
    return vector_sum


def scalar_multiplication(scalar, vector_1):
    """Defines multiplication of vector with scalar."""
    product = (scalar*vector_1[0], scalar*vector_1[1], scalar*vector_1[2])
    return product

def coord_illumnation(sphere, light, coords):
    """Determines the illumination value between 0 and 1 of a coordinate on the surface of the sphere."""
    illumination = dot_product(light, coords)/(sphere.radius**2)
    if illumination < 0:
        illumination = 0
    return illumination


def is_shadowed(sphere, light, coords):
    """Determines if the coordinate is shadowed by the cross section of the sphere orthogonal to lights direction.
    If shadowed, returns True. Else, False"""
    light_projection = scalar_multiplication(-dot_product(light.direction, coords), light.direction)
    light_point = vector_addition(coords, light_projection)
    if sphere.within_sphere(light_point):
        return True
    else:
        return False