# -----------------------------------------------------------------------------
# Copyright (2025) Alexandre B A Villares - BSD license
# Numpy flocking with py5 - revisiting sketch 2024_01_19
#
# Based on the boids flocking example from "From Pytnon to Numpy"
# Copyright (2017) Nicolas P. Rougier - BSD license
# More information at https://github.com/rougier/numpy-book
# -----------------------------------------------------------------------------
import numpy as np
import py5

WIDTH = 650
HEIGHT = 650
BOID_COUNT = 500
BOID_SIZE = 10


def constrain_magnitude(v, max_mag, *, min_mag=0.0):
    norm = np.linalg.norm(v, axis=1, keepdims=True)
    np.multiply(
        v,
        max_mag / norm,
        out=v,
        where=norm > max_mag,
    )

    if min_mag > 0:
        np.multiply(
            v,
            min_mag / norm,
            out=v,
            where=norm < min_mag,
        )

    return v


class Flock:
    def __init__(self, boid_count, width, height):
        self.width = width
        self.height = height
        self.min_velocity = 0.5
        self.max_velocity = 2.0
        self.max_acceleration = 0.03
        self.velocity = np.zeros((boid_count, 2), dtype=np.float32)
        self.position = np.zeros((boid_count, 2), dtype=np.float32)

        # initial random velocity
        angle = np.random.uniform(0, 2 * np.pi, boid_count)
        self.velocity[:, 0] = np.cos(angle)
        self.velocity[:, 1] = np.sin(angle)

        # initial random position in circle
        angle = np.random.uniform(0, 2 * np.pi, boid_count)
        radius = min(width, height) / 2 * np.random.uniform(0, 1, boid_count)
        self.position[:, 0] = width / 2 + np.cos(angle) * radius
        self.position[:, 1] = height / 2 + np.sin(angle) * radius

    def update(self):
        # max_acceleration = self.max_acceleration
        n = len(self.position)

        # subtract.outer(A, B) calculates the difference between
        # every value in A with every value in B
        dx = np.subtract.outer(self.position[:, 0], self.position[:, 0])
        dy = np.subtract.outer(self.position[:, 1], self.position[:, 1])
        distances = np.hypot(dx, dy)

        # Compute common distance masks
        separation_mask = (0 < distances) * (distances < 25)
        alignment_mask = (0 < distances) * (distances < 50)
        cohesion_mask = alignment_mask
        separation_count = np.maximum(separation_mask.sum(axis=1), 1)
        alignment_count = np.maximum(alignment_mask.sum(axis=1), 1)
        cohesion_count = alignment_count
        self.neighbor_count = alignment_count

        # Separation Force, keeps boids from getting too close
        mask, count = separation_mask, separation_count
        target = np.dstack((dx, dy))
        target = np.divide(
            target,
            distances.reshape(n, n, 1) ** 2,
            out=target,
            where=distances.reshape(n, n, 1) != 0,
        )
        steer = (target * mask.reshape(n, n, 1)).sum(axis=1) / count.reshape(n, 1)
        norm = np.linalg.norm(steer, axis=1, keepdims=True)
        steer = self.max_velocity * np.divide(steer, norm, out=steer, where=norm != 0)
        steer -= self.velocity

        separation_force = constrain_magnitude(steer, self.max_acceleration)

        # Alignment Force, keeps neighboring boids moving
        # in the same direction. Each boid's direction
        # is the average of its neighbors
        mask, count = alignment_mask, alignment_count
        target = np.dot(mask, self.velocity) / count.reshape(n, 1)

        # Compute steering
        norm = np.linalg.norm(target, axis=1, keepdims=True)
        target = self.max_velocity * np.divide(
            target, norm, out=target, where=norm != 0
        )
        steer = target - self.velocity

        alignment_force = constrain_magnitude(steer, self.max_acceleration)

        # Cohesion Force, keeps neighboring boids together
        # Boids steer towards the average neighbor position
        mask, count = cohesion_mask, cohesion_count
        target = np.dot(mask, self.position) / count.reshape(n, 1)

        # Compute steering
        desired = target - self.position
        norm = np.linalg.norm(desired, axis=1, keepdims=True)
        desired *= self.max_velocity / norm
        steer = desired - self.velocity

        cohesion_force = constrain_magnitude(steer, self.max_acceleration)

        # ---------------------------------------------------------------------
        acceleration = 1.5 * separation_force + alignment_force + cohesion_force
        self.velocity += acceleration

        self.velocity = constrain_magnitude(
            self.velocity, self.max_velocity, min_mag=self.min_velocity
        )

        # update position
        self.position += self.velocity

        # Wraparound window
        self.position += (self.width, self.height)
        self.position %= (self.width, self.height)


flock = Flock(BOID_COUNT, WIDTH, HEIGHT)


def setup():
    py5.size(WIDTH, HEIGHT)
    py5.no_stroke()


def draw():
    py5.background(0)
    flock.update()

    red_mask = flock.neighbor_count > 30
    orange_mask = (20 < flock.neighbor_count) * (flock.neighbor_count <= 30)
    yellow_mask = flock.neighbor_count <= 20
    draw_boids(flock, red_mask, "red")
    draw_boids(flock, orange_mask, "orange")
    draw_boids(flock, yellow_mask, "yellow")


def draw_boids(flock, mask, fill_color):
    position = flock.position[mask]
    velocity = flock.velocity[mask]

    # calculate the 3 vertices of each boid symbol
    norm_vel = velocity / np.linalg.norm(velocity, axis=1, keepdims=True)
    heading = norm_vel * BOID_SIZE
    perpend_a = norm_vel[:, ::-1].copy() * (BOID_SIZE / 3)
    perpend_a[:, 0] = -perpend_a[:, 0]
    perpend_b = norm_vel[:, ::-1].copy() * (BOID_SIZE / 3)
    perpend_b[:, 1] = -perpend_b[:, 1]
    right_points = position + perpend_a
    left_points = position + perpend_b
    head_points = position + heading
    triangles = np.hstack((left_points, right_points, head_points)).reshape(-1, 2)

    py5.fill(fill_color)
    with py5.begin_shape(py5.TRIANGLES):
        py5.vertices(triangles)  # type: ignore


py5.run_sketch()
