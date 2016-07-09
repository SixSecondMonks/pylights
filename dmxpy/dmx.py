from __future__ import print_function
import serial, sys

class Dmx:
    START_MSG = 0x7E
    LABEL     = 0x06
    START     = 0x00
    END_MSG   = 0xE7

    def __init__(self, port):
        self.device = port

        try:
            self.port = serial.Serial(port, baudrate = 115200, timeout = 1)
        except:
            print("Could not initialize device", self.port, ". Exiting.")
            sys.exit(1)

    def write(self, data):
        size = len(data) + 1
        packet = [Dmx.START_MSG, Dmx.LABEL, size & 255, (size >> 8) & 255, Dmx.START]
        packet += data
        packet.append(Dmx.END_MSG)
        packet = map(chr, packet)
        self.port.write(''.join(packet))

    def close(self):
        self.port.close()


