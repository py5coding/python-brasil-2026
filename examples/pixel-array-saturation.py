import py5

def setup():
    py5.size(800, 400)
    py5.background(0)
    img_path = "piscina.png"
    img = py5.load_image(img_path)
    img.load_np_pixels()
    pixels_array = img.np_pixels
    pixels_array[pixels_array > 128] = 255
    pixels_array[pixels_array < 128] = 0
    img.update_np_pixels()
    py5.image(img, 0, 0)
    py5.save_frame("saturated.png")

py5.run_sketch()
