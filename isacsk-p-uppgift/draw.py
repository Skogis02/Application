from tkinter import *
import classes
import Engine

width = 600
height = 600
radius = 50


def hexcolor(denary):
    """Creates a hexcolor on a greyscale. Returns a string on the format #ABABAB, where AB is a hexnumber."""
    value = round(255*denary)
    hexadecimal = hex(value)[2:4]
    if len(hexadecimal) == 1:
        hexadecimal = "0" + hexadecimal
    return "#" + hexadecimal + hexadecimal + hexadecimal


def draw_shadow(sphere, light, gui):
    """Draws the shadow cast by the sphere on the xy-plane. Returns None"""
    for x in range(-width//2, width//2):
        for y in range(-height//2, height//2):
            if Engine.is_shadowed(sphere, light, (x, y, -sphere.radius)):
                gui.image.put("#404040", (x+width//2, y+height//2))


def draw_sphere(sphere, light, gui):
    """Draws the illuminated sphere. Every coordinate has a color depending on the level of illumination.
    Returns None"""
    for x in range(-sphere.radius, sphere.radius):
        for y in range(-sphere.radius, sphere.radius):
            coords = sphere.on_sphere((x, y))
            if coords is not False:
                illumination = Engine.coord_illumnation(sphere, light.coords, coords)
                color = hexcolor(illumination)
                gui.image.put(color, (width//2+x, height//2+y))


def click(event, sphere, light, gui):
    """Changes light postition and draws new sphere if user has clicked within the sphere. Returns None"""
    if sphere.on_sphere((event.x - width/2, event.y - width/2)) is False:
        return
    gui.new_image(width, height)
    light.change_coords((event.x - width/2, event.y - height/2))
    draw_shadow(sphere, light, gui)
    draw_sphere(sphere, light, gui)


def main():
    """Creates gui, sphere and light. Draws scene and binds left mousebutton to click().
    Returns None, end of program."""
    gui = classes.Gui(width, height)
    sphere = classes.Sphere(radius)
    light = classes.LightVector(sphere, (0, 0))
    draw_shadow(sphere, light, gui)
    draw_sphere(sphere, light, gui)
    gui.canvas.bind("<Button-1>", lambda event: click(event, sphere, light, gui))
    mainloop()

main()