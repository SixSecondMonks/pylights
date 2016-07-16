from bibliopixel.drivers.serial_driver import LEDTYPE, DriverSerial
from bibliopixel.led import LEDStrip, LEDMatrix

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
            print("Could not initialize device", self.port, ".", sys.exc_info()[0], "Exiting.")
            sys.exit(1)


        self.led = LEDStrip(self.device)
        self.led.setMasterBrightness(16)

    def fix(self, data):
        self.device._update(data)

    def render(self):
        pass

    def close(self):
        print("off")
        self.device._update([0] * 3 * self.number)
        self.led.all_off()
