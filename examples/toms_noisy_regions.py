# Based on Tom Larrow's experiment at:
# https://codeberg.org/TomLarrow/creative-coding-experiments/src/branch/main/x_0049/x_0049.py

import numpy as np
import py5


def setup():
    py5.size(800, 800)
    py5.no_stroke()
    py5.color_mode(py5.HSB)


def draw():
    py5.no_loop()
    py5.background(150, 100, 100)
    margin = py5.width / 16  # Give us a margin on the right
    x = margin
    while x < py5.width - margin:
        w = py5.random_int(2, 7) * 5
        h = py5.height * py5.random_int(5, 10) / 12
        y = (py5.height - h) / 2
        if x + w > py5.width - margin:
            w = (py5.width - margin) - x
        py5.fill(w * 8, 200, 200)
        py5.rect(x, y, w, h)
        x += w

    # Now that we have the image above, lets add grain, but only to the parts
    # that aren't the background
    py5.load_np_pixels()  # Load the processing pixel array as an uint8 numpy array
    # Build a new numpy array the same size to hold our noise, and fill it with random values
    # It is an signed 16 array, so that it can handle negative numbers and
    # buffer overflows
    noise_pixels = np.random.randint(-50, 50, size=(py5.width, py5.height, 4))
    # np_pixels gives each pixel in an [A, R, G, B] format. We don't want to mess with the alpha, so setting
    # all the alpha values to zero, so that they don't change when we start
    # doing math on the array
    noise_pixels[:, :, 0] = 0
    # Add the contents of np_pixels to our noise_pixels array
    # This gives us an array where every pixel is adjusted by noise
    noise_pixels += py5.np_pixels
    # Because our noise_pixels array is a signed 16-bit integer it can have negative numbers or numbers greater than 255
    # So we clip them to stay in those bounds to avoid buffer overflows once
    # we go back to uint8
    noise_pixels = np.clip(noise_pixels, 0, 255)
    # the numpy where function lets us make decisions based on a condition
    # I know that pixel 0,0 is a background color, so I compare each pixel to 0,0 to see if it's the background or not
    # If it is the background, copy in the value for that pixel from np_pixels (which is just our background)
    # Otherwise, copy in the value from our noise_pixels
    # This is how we end up with only the foreground components having grain
    my_display = np.where(
        py5.np_pixels == py5.np_pixels[0, 0], py5.np_pixels, noise_pixels
    )
    py5.set_np_pixels(my_display)  # Copy our new array back to np_pixels
    # no need to explicitly call update_pixels() because set_np_pixels()
    # takes care of that for us
    # py5.update_pixels()


def key_pressed():
    py5.redraw()


py5.run_sketch()
