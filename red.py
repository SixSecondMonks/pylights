from pylights.program import Program
from animations.basic import ColorFade

class RedFade(Program):
    def __init__(self):
        super(RedFade, self).__init__('red fade', fps=30)

    def get_animation(self, led):
        hue = 0
        return ColorFade(hue, led)

def run():
    print('running red fade')
    RedFade()

if __name__ == "__main__":
    run()
