from pylights.program import Program
from animations.Rainbows import RainbowCycle

class Rainbow(Program):
    def __init__(self):
        super(Rainbow, self).__init__('rainbow')

    def get_animation(self, led):
        return RainbowCycle(led)

def run():
    print('running Rainbow')
    Rainbow()

if __name__ == "__main__":
    run()
