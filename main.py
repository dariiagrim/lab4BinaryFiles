import struct
import sys


class Pixel(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __mul__(self, other):
        return Pixel(self.r * other, self.g * other, self.b * other)

    def __add__(self, other):
        return Pixel(self.r + other.r, self.g + other.g, self.b + other.b)

    def __str__(self):
        return f"red: {self.r}, green: {self.g}, blue: {self.b}"


class Image(object):
    def __init__(self, file_name):
        self.width = 0
        self.height = 0
        self.pixels = []
        self._read(file_name)

    def _interpolate(self, pX, pY):
        x1 = int(pX)
        y1 = int(pY)
        x2 = min(x1 + 1, self.width - 1)
        y2 = min(y1 + 1, self.height - 1)

        lx = pX - x1
        ly = pY - y1

        bl = self.pixels[x1][y2]
        br = self.pixels[x2][y2]
        tl = self.pixels[x1][y1]
        tr = self.pixels[x2][y1]

        r1 = bl * lx + br * (1. - lx)
        r2 = tl * lx + tr * (1. - lx)

        return r1 * ly + r2 * (1. - ly)

    def _read(self, file_name):
        f = open(file_name, 'rb')
        f.seek(2)
        file_size = struct.unpack('<L', f.read(4))[0]
        f.seek(18)
        self.width, self.height = struct.unpack('<LL', f.read(8))
        self.pixels = [[Pixel(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)]
        f.seek(54)
        t = f.tell()
        i = j = 0
        while t < file_size and i < self.height and j < self.width:
            r, g, b = struct.unpack('<BBB', f.read(3))
            t = f.tell()
            self.pixels[i][j].r = r
            self.pixels[i][j].g = g
            self.pixels[i][j].b = b
            j += 1
            if j >= self.width:
                n = 4 - ((self.width * 3) % 4)
                f.read(n)
                t = f.tell()
                i += 1
                j = 0
        f.close()

    def write(self, file_name):
        f = open(file_name, "wb")
        f.write(struct.pack("<BB", ord("B"), ord("M")))
        pos = f.tell()
        f.write(struct.pack("<L", 0))
        f.write(struct.pack("<L", 0))
        f.write(struct.pack("<L", 54))
        f.write(struct.pack("<L", 40))
        f.write(struct.pack("<LL", self.width, self.height))
        f.write(struct.pack("<H", 1))
        f.write(struct.pack("<H", 24))
        f.write(struct.pack("<LLLLLL", 0, 0, 0, 0, 0, 0))
        for row in self.pixels:
            for pixel in row:
                f.write(struct.pack("<BBB", pixel.r, pixel.g, pixel.b))
            for _ in range(4 - ((self.width * 3) % 4)):
                f.write(struct.pack("<B", 0))
        file_size = f.tell()
        f.seek(pos)
        f.write(struct.pack("<L", file_size))
        f.close()


if __name__ == "__main__":
    image = Image(sys.argv[1])
    image.write(sys.argv[2])

