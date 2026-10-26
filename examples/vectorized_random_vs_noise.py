import numpy as np
import py5

noise_scale = 0.01


def setup():
    py5.size(400, 400)


def draw():
    py5.background(240)
    x_offset = 0  # py5.mouse_x

    np.random.seed(1001)
    all_xs = np.arange(py5.width)
    random_ys = np.random.uniform(0, py5.height / 2, py5.width)
    base_ys = np.zeros(py5.width)
    py5.lines(
        np.column_stack(
            [
                all_xs,  # xa
                base_ys,  # ya (all start at 0)
                all_xs,  # xb (same as xa)
                random_ys,  # yb the random
            ]
        )  # type: ignore
    )

    all_xs = np.arange(py5.width)
    base_ys = np.ones(py5.width) * (py5.height / 2)
    noise_values = py5.noise((x_offset + all_xs) * noise_scale)
    noise_ys = py5.lerp(py5.height / 2, py5.height, noise_values)

    py5.lines(
        np.column_stack(
            [
                all_xs,  # xa
                base_ys,  # ya (all start at height/2)
                all_xs,  # xb (same as xa)
                noise_ys,  # yb (from noise)
            ]
        )  # type: ignore
    )


def key_pressed():
    if py5.key == "s":
        py5.save_frame("###.png")


py5.run_sketch()
