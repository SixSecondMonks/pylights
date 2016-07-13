from bibliopixel.drivers.serial_driver import LEDTYPE, DriverSerial

import sys

class PixelPusher:
    DEFAULT_PORT = "/dev/ttyACM0"
    DEFAULT_KIND = "WS2812B"

    def __init__(self, port=DEFAULT_PORT, kind=DEFAULT_KIND, number=100):
        self.port = port
        self.number = number
        self.kind = kind
        try:
            self.device = DriverSerial(num=number, type=getattr(LEDTYPE, kind), dev=port)
        except:
            print("Could not initialize device", self.port, ". Exiting.")
            sys.exit(1)

    def fix(self, data):
        self.device._update(data)

    def render(self):
        pass
