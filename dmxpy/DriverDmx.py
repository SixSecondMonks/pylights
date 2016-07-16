from __future__ import print_function
from bibliopixel.drivers.driver_base import *
import serial, sys

class Fixture:
    @classmethod
    def create_packet(cls, r, g, b):
        packet = [0] * 8
        packet[3] = 0xff
        packet[4] = r
        packet[5] = g
        packet[6] = b
        return packet

class DriverDmx(DriverBase):
    START_MSG = 0x7E
    LABEL     = 0x06
    START     = 0x00
    END_MSG   = 0xE7

    def __init__(self, num, port='/dev/ttyS0'):
        super(DriverDmx, self).__init__(num)
        self.port = port
        self.intensity = 255

        try:
            self.device = serial.Serial(port, baudrate=115200, timeout=1)
        except:
            print("Could not initialize device", self.port, ". Exiting.")
            sys.exit(1)

    def update(self, data):
        self._fixData(data)
        p = Fixture.create_packet(self._buf[0], self._buf[1], self._buf[2])
        size = len(p) + 1
        packet = [DriverDmx.START_MSG, DriverDmx.LABEL, size & 255, (size >> 8), DriverDmx.START]
        packet += p
        packet.append(DriverDmx.END_MSG)
        print(packet)
        packet = map(chr, packet)
        self.device.write(''.join(packet))

    def setMasterBrightness(self, brightness):
        self.intensity = brightness


