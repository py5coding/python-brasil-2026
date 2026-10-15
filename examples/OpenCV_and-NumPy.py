import cv2
import numpy as np
import py5

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

py5_img = None


def setup():
    global py5_img
    py5.size(VIDEO_WIDTH, VIDEO_HEIGHT)
    py5_img = py5.create_image(VIDEO_WIDTH, VIDEO_HEIGHT, py5.ARGB)


def draw():
    # set red background
    py5.background(200, 0, 0)
    # frame is a numpy array dimensions (h, w, 3)
    _, frame = cap.read()
    # create alpha mask based on grayscale values
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    alpha = np.where(frame_gray < 128, 255, 0)
    # combine frame with alpha channel
    frame_w_alpha = np.dstack([frame, alpha])
    # update image with new pixels
    py5_img.set_np_pixels(frame_w_alpha, bands="BGRA")
    # red background visible through parts of the webcam image
    py5.image(py5_img, 0, 0)


def exiting():
    print("Release webcam")
    cap.release()


py5.run_sketch()
