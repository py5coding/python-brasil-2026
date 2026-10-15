# Experiment inspired by the "Particle Life" strategies
# Presented by John @introscopia at Noite de Processing

import numpy as np
import py5
from scipy.spatial import KDTree

WIDTH = 800
HEIGHT = 800

PARTICLE_COUNT = 200
SPECIES_COUNT = 5
COLOR_STEP = 256 / SPECIES_COUNT
INTERACTION_DIST = 100
SIZE_SQR = 10  # "squared" particle size
force_rules = np.random.uniform(-3, 3, (SPECIES_COUNT, SPECIES_COUNT))


class Particle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.pos = np.array([py5.random(width), py5.random(height)])
        self.vel = np.array([py5.random(-1, 1), py5.random(-1, 1)])
        self.especie = int(py5.random(SPECIES_COUNT))

    def update(self, tree):
        self.pos = (self.pos + self.vel) % (self.width, self.height)
        self.vel *= 0.95

        # query tree to get points in same cluster
        for i in tree.query_ball_point(self.pos, r=INTERACTION_DIST):
            other = particles[i]
            force = self.pos - other.pos
            dsq = (force**2).sum()
            if dsq < INTERACTION_DIST**2:
                if dsq < SIZE_SQR:
                    # prevent particles from being too close together
                    m = py5.remap(dsq, 0, SIZE_SQR, 1, 0)
                    force_mag = m
                else:
                    # attraction force is stronger for particles that
                    # are farther apart
                    m = py5.remap(dsq, 0, INTERACTION_DIST**2, 0.001, 0)
                    lm = force_rules[self.especie][other.especie] * m
                    force_mag = lm

                self.vel += force * force_mag

        # display particle
        py5.stroke(self.especie * COLOR_STEP, 255, 255)
        py5.point(*self.pos)


particles = [Particle(WIDTH, HEIGHT) for _ in range(PARTICLE_COUNT)]
trails = False


def setup():
    py5.size(WIDTH, HEIGHT)
    py5.no_smooth()
    py5.color_mode(py5.HSB)

    py5.stroke_weight(10)
    py5.stroke_cap(py5.PROJECT)

    py5.background(0)


def draw():
    if trails:
        py5.no_stroke()
        py5.fill(32, 16)
        py5.rect(0, 0, py5.width, py5.height)
    else:
        py5.background(0)

    tree = KDTree(tuple(p.pos for p in particles))
    for p in particles:
        p.update(tree)


def key_pressed():
    global trails
    if py5.key == "t":
        trails = not trails


py5.run_sketch()
