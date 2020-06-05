"""Image and bitmap processing utils"""
from PIL import Image
import numpy as np

# Scale down images larger than this
MAX_SIZE = 1000


def read_image(fname: str) -> (Image.Image, np.array):
    """Read file, return image and its bitmap array"""
    im = Image.open(fname)
    while im.width > MAX_SIZE or im.height > MAX_SIZE:
        im = im.resize((im.width // 2, im.height // 2))
    bitmap = im.convert('1')
    a = np.asarray(bitmap)
    a, pos = shrink(a)
    im = im.crop((pos[1], pos[0], pos[1] + a.shape[1], pos[0] + a.shape[0]))
    return im, a


def shrink_vertically(c: np.array, p: int):
    top, bottom = 0, len(c)
    while top < bottom:
        if all(c[top]):
            top += 1
            p += 1
        elif all(c[bottom - 1]):
            bottom -= 1
        else:
            break
    return c[top:bottom], p


def values_around(a, i, j):
    return [a[i + x, j + y]
            for x in range(-1, 2) for y in range(-1, 2)
            if (x, y) != (0, 0)
            and 0 <= i + x < a.shape[0]
            and 0 <= j + y < a.shape[1]]


def shrink(c, pos=(0, 0)):
    """Crop out empty margins of a bitmap"""
    # Shrink one pixel from each side
    c = np.copy(c[1:-1, 1:-1])
    pos = (pos[0] + 1, pos[1] + 1)
    c = remove_noise(c)
    # Shrink vertically
    c, vpos = shrink_vertically(c, pos[0])
    # Shrink horizontally
    t = np.transpose(c)
    t, hpos = shrink_vertically(t, pos[1])
    return np.transpose(t), (vpos, hpos)


def remove_noise(c):
    c = np.copy(c)
    # Remove isolated pixels
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):
            if not c[i, j] and all(values_around(c, i, j)):
                c[i, j] = True
    return c


def show_cells(a, cells):
    """Display bitmap with outlines of all cells; for debugging only"""
    im = Image.fromarray(a).convert('RGB')
    color = 0x0000ff
    for c, coords, _ in cells:
        for i in range(-1, c.shape[0] + 1):
            im.putpixel((coords[1] - 1, coords[0] + i), color)
            im.putpixel((coords[1] + c.shape[1], coords[0] + i), color)
        for i in range(-1, c.shape[1] + 1):
            im.putpixel((coords[1] + i, coords[0] - 1), color)
            im.putpixel((coords[1] + i, coords[0] + c.shape[0]), color)
    im.show()