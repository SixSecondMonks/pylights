from pylights.program import Program
from animations.RainbowsMixed import RainbowCycleAudio

class VolumeRainbow(Program):
    def __init__(self):
        super(VolumeRainbow, self).__init__('rainbow')

    def get_animation(self, led):
        return RainbowCycleAudio(led)

def run():
    print('running VolumeRainbow')
    VolumeRainbow()

if __name__ == "__main__":
    run()
