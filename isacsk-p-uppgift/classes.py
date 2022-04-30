import math
import Engine
from tkinter import*


class Sphere:
    """Defines a sphere with center at origin and arbitrary radius."""
    def __init__(self, radius):
        self.center = (0, 0, 0)
        self.radius = radius


    def on_sphere(self, xy_tuple):
        """"If possible, returns z so that (x,y,z) is on the surface of the sphere. Else, returns False."""
        z_square = self.radius**2 - xy_tuple[0]**2 - xy_tuple[1]**2
        if z_square >= 0:
            z = math.sqrt(z_square)
            return xy_tuple[0], xy_tuple[1], z
        else:
            return False

    def within_sphere(self, coords):
        """Returns true if coords are within the sphere. Else, returns False."""
        if 0 <= self.radius**2 - coords[0] ** 2 - coords[1]**2 - coords[2]**2:
            return True
        else:
            return False


class LightVector:
    """Defines a vector from origin to the surface of a sphere."""
    def __init__(self, sphere, xy_tuple):
        self.sphere = sphere
        self.coords = sphere.on_sphere(xy_tuple)
        self.direction = Engine.scalar_multiplication(sphere.radius**(-1), self.coords)

    def change_coords(self, xy_tuple):
        """Redefines the vector according to new coordinates"""
        self.coords = self.sphere.on_sphere(xy_tuple)
        self.direction = Engine.scalar_multiplication(self.sphere.radius ** (-1), self.coords)


class Gui:
    """Creates a Gui that can display images and bind callbacks to functions."""
    def __init__(self, width, height):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=width, height=height, bg="white")
        self.canvas.pack()
        self.image = PhotoImage(width=width, height=height)
        self.canvas.create_image((width // 2, height // 2), image=self.image, state="normal")

    def new_image(self, width, height):
        """Deletes existing picture and creates a new blank one."""
        self.canvas.delete("all")
        self.image = PhotoImage(width=width, height=height)
        self.canvas.create_image((width // 2, height // 2), image=self.image, state="normal")


class Matrix:
    """Defines a matrix centered around the origin."""
    def __init__(self, width, height):
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        self.width = width
        self.height = height
        self.zero_element = (width//2, height//2)
        matrix = []
        for x in range(self.width):
            matrix.append([])
            for y in range(self.height):
                matrix[x].append("   ")
        self.matrix = matrix