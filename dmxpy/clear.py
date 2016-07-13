from program import Program

class Clear(Program):
    def __init__(self):
        super(Clear, self).__init__('clear')

    def initial_data(self):
        return {}

    def iterative_data(self):
        return self.initial_data()

if __name__ == "__main__":
    Clear()
