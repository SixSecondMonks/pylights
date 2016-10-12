from pylights.program import Program
from animations.Wave import Wave
from bibliopixel import colors

class Wavey(Program):
    def __init__(self):
        super(Wavey, self).__init__('wave', fps=5)

    def get_animation(self, led):
	color = colors.color_scale(colors.Red, 75)
        return Wave(led, color, 2)

def run():
    print('running Wavey')
    Wavey()

if __name__ == "__main__":
    run()
