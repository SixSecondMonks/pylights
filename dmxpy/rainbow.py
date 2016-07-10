from program import Program
from util import create_hue

class Rainbow(Program):
    def __init__(self):
        self.iteration = 0

    def initial_data(self):
        return dict([('intensity', 100), ('speed', 0xff), ('red', 0x0), ('blue', 0x0), ('green', 0xff)])

    def iterative_data(self):
        data = self.initial_data()
        (r, g, b) = create_hue(self.iteration)
        self.iteration += 1
        data['red'] = r
        data['green'] = g
        data['blue'] = b
        return data
