from pylights.program import Program
from animations.basic import RotatingColors

class SnakeProgram(Program):
    def __init__(self):
        # can do 90
        super(SnakeProgram, self).__init__('snake program', fps=1)

    def get_animation(self, led):
        hue = 0
        return RotatingColors([50, 169, 100, 169, 50], led)

def run():
    print('running red fade')
    SnakeProgram()

if __name__ == "__main__":
    run()
