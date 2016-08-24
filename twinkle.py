from pylights.program import Program
from animations.WhiteTwinkle import WhiteTwinkle

class WhiteTwinkleProgram(Program):
    def __init__(self):
        super(WhiteTwinkleProgram, self).__init__('whitetwinkle')

    def get_animation(self, led):
        return WhiteTwinkle(led)

def run():
    print('running white twinkle')
    WhiteTwinkleProgram()

if __name__ == "__main__":
    run()
