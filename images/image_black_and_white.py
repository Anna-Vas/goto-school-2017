from PIL import Image

# Open image and load pixels
im = Image.open('ironman.jpg')
im.show()

pixels = im.load()

# Black and white filter
for i in range(im.width):
    for j in range(im.height):
        r, g, b = pixels[i, j]
        r = g = b
        pixels[i, j] = (r, g, b)

# Show result
im.show()
