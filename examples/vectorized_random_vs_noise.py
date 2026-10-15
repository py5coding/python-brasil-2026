import py5
import numpy as np

noise_scale = 0.01

def setup():
    py5.size(400, 400)

def draw():
    py5.background(240)
    x_offset = 0 # py5.mouse_x

#     py5.random_seed(1001)  # para 'travar' o random()
#     for x in range(py5.width):
#         y = py5.random(py5.height / 2)
#         py5.line(x, 0, x, y)

    np.random.seed(1001)
    all_xs = np.arange(py5.width)
    random_ys = np.random.uniform(0, py5.height / 2, py5.width)
    base_ys = np.zeros(py5.width)
    py5.lines(np.column_stack([
        all_xs,     # xa
        base_ys,    # ya (all start at 0)
        all_xs,     # xb (same as xa)
        random_ys   # yb the random
    ]))

#     for x in range(py5.width):
#         n = py5.noise((x_offset + x) * noise_scale)
#         y = py5.lerp(py5.height / 2, py5.height, n)
#         # y = height / 2 + (height / 2) * n
#         py5.line(x, py5.height / 2, x, y)

    all_xs = np.arange(py5.width)
    base_ys = np.ones(py5.width) * (py5.height / 2)
    noise_values = py5.noise((x_offset + all_xs) * noise_scale)
    noise_ys = py5.lerp(py5.height / 2, py5.height, noise_values)

    py5.lines(np.column_stack([
        all_xs,   # xa
        base_ys,  # ya (all start at height/2)
        all_xs,   # xb (same as xa)
        noise_ys  # yb (from noise)
    ]))

def key_pressed():
    if py5.key == 's':
        py5.save_frame('###.png')
        
py5.run_sketch()
