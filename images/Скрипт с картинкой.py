from PIL import Image

im = Image.open('ironman.jpg')
im.show()

pixels = im.load()

for i in range(im.width):
    for j in range(im.height):
        r, g, b = pixels[i, j]
        r = min(r + 100, 255)
        pixels[i, j] = (r, g, b)

im.show()
