from pylights.program import Program
from animations.YellowTwinkle import YellowTwinkle

class YellowTwinkleProgram(Program):
    def __init__(self):
        super(YellowTwinkleProgram, self).__init__('whitetwinkle')

    def get_animation(self, led, density=5):
        return YellowTwinkle(led)

def run():
    print('running white twinkle')
    YellowTwinkleProgram()

if __name__ == "__main__":
    run()
