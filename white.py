from pylights.program import Program
from animations.basic import ColorFill

class SnakeProgram(Program):
    def __init__(self):
        # can do 90
        super(SnakeProgram, self).__init__('snake program', fps=5)

    def get_animation(self, led):
        hue = 0
        return ColorFill(led, 255, 255, 255)

def run():
    print('running all white')
    SnakeProgram()

if __name__ == "__main__":
    run()
