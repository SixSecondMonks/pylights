from pylights.program import Program
from animations.Rainbows import RainbowCycleAudio

class Rainbow(Program):
    def __init__(self):
        super(Rainbow, self).__init__('rainbow')

    def get_animation(self, led):
        return RainbowCycleAudio(led)

if __name__ == "__main__":
    Rainbow()
