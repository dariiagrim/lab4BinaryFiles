class Pixel(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return f"red: {self.r}, green: {self.g}, blue: {self.b}"


pixel = Pixel(100, 200, 40)
assert str(pixel) == "red: 100, green: 200, blue: 40"


