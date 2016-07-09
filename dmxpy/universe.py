from __future__ import print_function

class Universe:
    NUM_CHANNELS = 512

    def __init__(self, port):
        self.port = port

    def inspect(self):
        print("Using port", self.port, "!")
