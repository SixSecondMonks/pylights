from __future__ import print_function
import serial, sys, time

class Dmx:
    DEFAULT_PORT = "/dev/ttyUSB0"
    START_MSG = 0x7E
    LABEL     = 0x06
    START     = 0x00
    END_MSG   = 0xE7

    def __init__(self, port=DEFAULT_PORT):
        self.device = port
        try:
            self.port = serial.Serial(port, baudrate = 115200, timeout = 1)
        except:
            print("Could not initialize device", self.device, ". Exiting.")
            sys.exit(1)

    def write(self, data):
        size = len(data) + 1
        packet = [Dmx.START_MSG, Dmx.LABEL, size & 255, (size >> 8) & 255, Dmx.START]
        packet += data
        packet.append(Dmx.END_MSG)
        packet = map(chr, packet)
        self.port.write(''.join(packet))

    def test(self):
        blank = [0,0,0,0,0,0,0,0]
        red = [100,0,0,255,255,0,0,0]
        purple = [100,0,0,255,255,0,255,0]

        x = 0
        while True:
            command = []
            for y in range(1,3):
                command += blank
            if x % 2 == 0:
                command += red
                x += 1
            else:
                command += purple
                x -= 1
            self.write(command)
            time.sleep(1)

    def testa(self):
        purple = [255,0,0,255,255,0,255,0]
        blank = [0,0,0,0,0,0,0,0]
        for x in range(1,18):
            command = []
            for y in range(1,x):
                command += blank
            command += purple
            self.write(command)
            print("sent", command, "to address", x)
            time.sleep(1)

    def clear(self):
        self.write([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

    def close(self):
        self.port.close()
