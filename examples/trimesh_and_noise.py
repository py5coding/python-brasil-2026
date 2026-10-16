# Alexandre B A Villares -https://abav.lugaralgum.com/sketch-a-day

from itertools import product

import numpy as np
import py5
import trimesh
from py5_tools import animated_gif

A, B, C = 30, 30, 2
W = 10
step = 0.1


def setup():
    global mesh
    py5.size(500, 500, py5.P3D)
    position_map = {
        (i, j, k): n
        for n, (i, j, k) in enumerate(product(range(A), range(B), range(C)))
    }
    m = (py5.width - W * A) / 2
    vs = np.array(
        [
            (
                m + i * W + W / 2,
                m + j * W + W / 2,
                k * W + W * 2 * py5.os_noise(i * step, j * step),
            )
            for i, j, k in product(range(A), range(B), range(C))
        ]
    )

    i_vals, j_vals, k_vals = np.meshgrid(
        np.arange(A), np.arange(B), np.arange(C), indexing="ij"
    )
    i_flat = i_vals.flatten()
    j_flat = j_vals.flatten()
    k_flat = k_vals.flatten()
    noise_vals = py5.os_noise(i_flat * step, j_flat * step)  # vectorized noise call
    vs = np.column_stack(
        [
            m + i_flat * W + W / 2,
            m + j_flat * W + W / 2,
            k_flat * W + W * 2 * noise_vals,
        ]
    )

    i_vals, j_vals, k_vals = np.mgrid[0:A, 0:B, 0:C]
    noise_vals = py5.os_noise(i_vals.ravel() * step, j_vals.ravel() * step)
    vs = np.column_stack(
        [
            m + i_vals.ravel() * W + W / 2,
            m + j_vals.ravel() * W + W / 2,
            k_vals.ravel() * W + W * 2 * noise_vals,
        ]
    )

    # organizes the faces in a pattern with nice diagonal lines
    faces = []
    for i, j in product(range(A), range(B)):
        for k in range(C):
            if (i + 1, j + 1, k) in position_map:
                va = position_map[i, j, k]
                vb = position_map[i + 1, j, k]
                vc = position_map[i + 1, j + 1, k]
                vd = position_map[i, j + 1, k]
                if (i + j) % 2:
                    faces.append([va, vb, vc])
                    faces.append([va, vc, vd])
                else:
                    faces.append([va, vb, vd])
                    faces.append([vb, vc, vd])
            if (i == 0 or i == A - 1) and (i, j + 1, k + 1) in position_map:
                va = position_map[i, j, k]
                vb = position_map[i, j + 1, k]
                vc = position_map[i, j + 1, k + 1]
                vd = position_map[i, j, k + 1]
                faces.append([va, vb, vc])
                faces.append([va, vc, vd])
            if (j == 0 or j == B - 1) and (i + 1, j, k + 1) in position_map:
                va = position_map[i, j, k]
                vb = position_map[i + 1, j, k]
                vc = position_map[i + 1, j, k + 1]
                vd = position_map[i, j, k + 1]
                faces.append([va, vb, vc])
                faces.append([va, vc, vd])

    faces = np.array(faces)
    mesh = trimesh.Trimesh(vertices=vs, faces=faces)


def key_pressed():
    animated_gif("out.gif", duration=5 / 60, frame_numbers=range(1, 361, 5))


def draw():
    py5.background(0, 100, 0)
    py5.lights()
    py5.translate(py5.width / 2, py5.height / 2)
    py5.rotate_x(py5.radians(py5.frame_count))  # type: ignore
    py5.rotate_y(py5.radians(45))  # type: ignore
    py5.translate(-py5.width / 2, -py5.height / 2)
    py5.fill(240)
    py5.shape(py5.convert_cached_shape(mesh, facet_edges=False))


py5.run_sketch()
