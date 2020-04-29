import struct


class Pixel(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return f"red: {self.r}, green: {self.g}, blue: {self.b}"


class Image(object):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.pixels = []

    def _read(self, file_name):
        f = open(file_name, 'rb')
        f.seek(2)
        file_size = struct.unpack('<L', f.read(4))[0]
        f.seek(18)
        self.width, self.height = struct.unpack('<LL', f.read(8))
        f.close()

image = Image()
image._read('bmp.bmp')
print(image.width, image.height)
