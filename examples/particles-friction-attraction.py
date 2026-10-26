import numpy as np
import py5

N = 1000
WIDTH, HEIGHT = 600, 400
ACCELERATION_SCALE = 4
VELOCITY_SCALE = 0.25
FRICTION_FACTOR = 1 - 0.001

# set initial positions and velocities
pos = np.random.uniform([0, 0], [WIDTH, HEIGHT], size=(N, 2))
initial_headings = np.random.uniform(0, 2 * np.pi, size=N)
vel = (
    np.column_stack([np.cos(initial_headings), np.sin(initial_headings)])
    * np.random.uniform(-5, 5, size=N)[:, None]
)


def setup():
    py5.size(WIDTH, HEIGHT)
    py5.stroke_weight(5)


def draw():
    global pos, vel
    py5.background(240)

    # vectors pointing towards mouse position from each particle
    v_mouse = np.array([py5.mouse_x, py5.mouse_y]) - pos
    # attraction force is closest for particles near the mouse
    acc = v_mouse / (v_mouse**2).sum(axis=1)[:, None]

    # update particle velocity and position
    vel = vel + ACCELERATION_SCALE * acc
    vel *= FRICTION_FACTOR
    pos = pos + VELOCITY_SCALE * vel
    pos %= (WIDTH, HEIGHT)  # wrap edges

    # draw updated points
    py5.points(pos)  # type: ignore


py5.run_sketch()
