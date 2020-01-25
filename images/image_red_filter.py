from PIL import Image

# Open image and load pixels
im = Image.open('ironman.jpg')
im.show()

pixels = im.load()

# Red filter
for i in range(im.width):
    for j in range(im.height):
        r, g, b = pixels[i, j]
        r = min(r + 100, 255)
        pixels[i, j] = (r, g, b)

# Show results
im.show()
