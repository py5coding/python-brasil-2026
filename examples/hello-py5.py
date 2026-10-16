import py5  # check out https://github.com/py5coding 
from collections import deque  # a double-ended queue

history = deque(maxlen=512)  # mouse dragged positions

def setup():   # py5 will call this once to set things up
    py5.size(600, 400)
    py5.no_stroke()
    py5.color_mode(py5.HSB)

def draw():   # py5 will call this in a loop
    py5.background(51)
    for i, (x, y) in enumerate(history):
        py5.fill(i / 2, 255, 255, 128)
        py5.circle(x, y, 8 + i / 16)
    history.rotate(-1)

def mouse_dragged():  # py5 will call this when you drag the mouse
    history.append((py5.mouse_x, py5.mouse_y))
    
py5.run_sketch()