import numpy as np
import py5

N = 1000
WIDTH, HEIGHT = 600, 400
step = 0.2
friction_factor = 1 - 0.001

pos = np.random.uniform([0, 0], [WIDTH, HEIGHT], size=(N, 2))  # .astype(np.float32)
# vel = np.random.uniform(-5, 5, size=(N, 2)) #.astype(np.float32)
headings = np.random.uniform(0, 2 * np.pi, size=N)
vel = (
    np.column_stack([np.cos(headings), np.sin(headings)])
    * np.random.uniform(-5, 5, size=N)[:, None]
)


def setup():
    py5.size(WIDTH, HEIGHT)
    py5.stroke_weight(5)


def draw():
    global pos, vel
    py5.background(240)

    v_mouse = np.array([py5.mouse_x, py5.mouse_y]) - pos  # vector towards mouse
    squared_mouse_dist = (
        np.sum(v_mouse * v_mouse, axis=1) + 1
    )  # avoiding 0s and higher speeds
    acc = 10 * v_mouse / squared_mouse_dist[:, None]
    vel = vel + acc * step
    vel *= friction_factor
    pos = pos + vel * step
    pos %= (WIDTH, HEIGHT)  # wrap edges
    py5.points(pos)  # draw

    py5.window_title(f"{py5.get_frame_rate():f}")


py5.run_sketch()
