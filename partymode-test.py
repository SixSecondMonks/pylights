from pylights.program import Program
from BiblioPixelAnimations.strip import Wave as PartyMode
import bibliopixel.colors as colors

SCALE=64

def convert(arr):
    return [colors.color_scale(x, SCALE) for x in arr]

def convert_one(c):
    return colors.color_scale(c, SCALE)

class PartyModeProgram(Program):
    def __init__(self):
        super(PartyModeProgram, self).__init__('whitetwinkle')

    def get_animation(self, led):
        return PartyMode.Wave(led, convert_one(colors.Orange), 0.0002)

def run():
    print('running party mode')
    PartyModeProgram()

if __name__ == "__main__":
    run()
