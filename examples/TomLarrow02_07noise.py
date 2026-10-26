"""
Adapted from Tom Larrow's example: 
https://codeberg.org/TomLarrow/creative-coding-experiments/src/branch/main/x_0000/x_0057

«An exploration into using numpy to speed up noise in py5
A recreation of https://github.com/jdf/processing.py/blob/master/mode/examples/Basics/Math/Noise3D/Noise3D.pyde
using numpy examples from https://py5coding.org/how_tos/generate_noise_values.html»
"""

import py5
import numpy as np

# How far apart the noise values will be. Lower numbers are more gradual
noise_increment = 0.02

def setup():
    global mesh_x, mesh_y
    py5.size(400, 400)
    # Builds two 2D arrays, mesh_x and mesh_y which have the dimensions of width x height
    # mesh_x has the values of the x position * noise_increment in the x direction, and is
    # duplicated for every y row, mesh_y has the values of the y position * noise_increment in the y
    # direction, and is duplicated for every x column
    mesh_x, mesh_y = np.meshgrid(
        np.arange(0, py5.width * noise_increment, noise_increment),
        np.arange(0, py5.height * noise_increment, noise_increment),
    )

def draw():
    # The next line essentially loops through screen width and the screen height and
    # generates a value between 0 and 255 for each point. However because  we're passing
    # in the arrays mesh_x and mesh_y, it is generating an array output all at once instead
    # of calling os_noise over and over in a loop. This dramatically improves performance
    out = py5.remap(
        py5.os_noise(mesh_x, mesh_y, py5.frame_count * noise_increment), -1, 1, 0, 255
    )
    # Now that we have an array with the output, set the sketch's main canvas with it
    # bands = "L" is for a greyscale image since r,g, and b would all be the same value
    py5.set_np_pixels(out, bands="L")  # type: ignore
    # Write the framerate to the window tile to see the effect of the
    # optimization
    py5.window_title(str(round(py5.get_frame_rate(), 1)))

py5.run_sketch()
