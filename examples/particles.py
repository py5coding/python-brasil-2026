import numpy as np
import py5
from py5_tools import animated_gif

N = 100
WIDTH = 600
pos = np.random.uniform(0, WIDTH, size=(N, 2))
vel = np.random.uniform(-2, 2, size=(N, 2))

def setup():
    py5.size(WIDTH, WIDTH)
    py5.stroke_weight(5)

def draw():
    global pos
    py5.background(240)
    py5.points(pos)  # type: ignore
    pos += vel
    pos %= WIDTH

def key_pressed():
    animated_gif('out.gif', count=100, period=0.1, duration=0.1)

py5.run_sketch()
