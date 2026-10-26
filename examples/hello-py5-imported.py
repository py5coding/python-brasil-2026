# não precisa import py5 e run_sketch no "imported mode"
from collections import deque 

history = deque(maxlen=512)  # histórico das posições

def setup():   
    size(600, 400)
    no_stroke()
    color_mode(HSB)

def draw():  # laço principal do py5
    background(51)
    for i, (x, y) in enumerate(history):
        fill(i / 2, 255, 255, 128)
        circle(x, y, 8 + i / 16)
    history.rotate(-1)

def mouse_dragged():  # ao arrastar o mouse
    history.append((mouse_x, mouse_y))