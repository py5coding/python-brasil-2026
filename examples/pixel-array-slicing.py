import numpy as np
import py5

def setup():
    py5.size(800, 400)
    py5.background(0)
    img_path = 'swimming-pool.png' 
    img = py5.load_image(img_path)
    img.load_np_pixels()
    print(img.np_pixels.shape) # shape is (400, 800, 4)
    pa = img.np_pixels 
    pa[:, 400:, 1] = 0
    pa[:, :, 2] = 0
    img.update_np_pixels()
    py5.image(img, 0, 0)
    
    py5.save_frame('red-blue-swimming-pool.png')
  
py5.run_sketch()