import Engine
import classes
import math

symbols = ((0, " M "), (0.3, " * "), (0.5, " + "), (0.7, " - "), (0.9, " . "), (1, "   "))

def light_symbol(illumination):
    """Returns appropriate symbol for given illumination as a string."""
    for i in range(6):
        if illumination <= symbols[i][0]:
            return symbols[i][1]
    return False


def print_matrix(matrix):
    """Prints each row of the matrix to create the a picture. Returns None."""
    for column in range(matrix.width):
        string = ""
        for row in range(matrix.height):
            string = string + str(matrix.matrix[column][row])
        print(string)


def draw_shadow(sphere, light, matrix):
    """Draws the shadow cast by the sphere onto the xy-plane. Returns None."""
    for column in range(matrix.width):
        for row in range(matrix.height):
            if Engine.is_shadowed(sphere, light, (column-matrix.zero_element[0], row-matrix.zero_element[1], -sphere.radius)):
                matrix.matrix[row][column] = " ` "


def draw_sphere(sphere, light, matrix):
    """Draws the illuminated sphere. Returns None."""
    for column in range(matrix.width):
        for row in range(matrix.height):
            coords = sphere.on_sphere((column - matrix.zero_element[0], row - matrix.zero_element[1]))
            if coords is not False:
                illumination = Engine.coord_illumnation(sphere, light.coords, coords)
                matrix.matrix[row][column] = light_symbol(illumination)


def main():
    """Prompts user for data: Radius, x and y coordinate for light.
    Creates a matrix, a sphere and a light vector. Prints a picture of the scene. Returns None, end of program"""
    while True:
        radius = int(input("Enter a sphere-radius between (not including) 0 and 100:"))
        if not 0 < radius < 100:
            print("Incorrect radius!")
        else:
            break
    sphere = classes.Sphere(radius)
    while True:
        light_x = int(input("Enter light x-coordinate between (not including) " + str(-sphere.radius) + " and " + str(sphere.radius) + ":"))
        light_y_bound = int(math.sqrt(sphere.radius**2 - light_x**2))
        light_y = int(input("Enter light y-coordinate between (not including) " + str(-light_y_bound) + " and " + str(light_y_bound)+":"))
        on_sphere_coords = sphere.on_sphere((light_x, light_y))
        if on_sphere_coords is False or on_sphere_coords[2] == 0:
            print("Incorrect values!")
        else:
            break
    matrix = classes.Matrix(100, 100)
    light = classes.LightVector(sphere, (light_x, light_y))
    draw_shadow(sphere, light, matrix)
    draw_sphere(sphere, light, matrix)
    print_matrix(matrix)

main()