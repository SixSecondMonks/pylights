from __future__ import print_function
import serial, sys, time
import socket

class DmxConnection:
    START_MSG = 0x7E
    LABEL     = 0x06
    START     = 0x00
    END_MSG   = 0xE7

    def packetize(self, data):
        size = len(data) + 1
        packet = [DmxConnection.START_MSG, DmxConnection.LABEL, size & 255, (size >> 8), DmxConnection.START]
        packet += data
        packet.append(DmxConnection.END_MSG)
        return map(chr, packet)

    def write(self, data):
        pass

    def close(self):
        pass

class DmxSerial(DmxConnection):
    DEFAULT_PORT = "/dev/ttyUSB0"

    def __init__(self, port=DEFAULT_PORT):
        self.port = port

        try:
            self.device = serial.Serial(port, baudrate=115200, timeout=1)
        except:
            print("Could not initialize device", self.port, ". Exiting.")
            sys.exit(1)

    def write(self, data):
        self.device.write(data)

    def close(self):
        self.device.close()

class DmxTcp(DmxConnection):
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 9999

    def __init__(self, ip=DEFAULT_HOST, port=DEFAULT_PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def write(self, data):
        self.socket.send(data)

    def close(self):
        self.socket.close()

class Dmx:
    START_MSG = 0x7E
    LABEL     = 0x06
    START     = 0x00
    END_MSG   = 0xE7

    def __init__(self, destination=DmxSerial.DEFAULT_PORT, tcp_port=None):
        self.packets = []
        if tcp_port is None:
            self.connection = DmxSerial(destination)
        else:
            self.connection = DmxTcp(destination, tcp_port)

    def fix(self, offset, data):
        print("fix", data)
        self.packets.append((offset, data))

    def render(self):
        maxsize = max(map(lambda (o, d): o + len(d), self.packets))
        data = [0 for _ in range(maxsize)]
        for (offset, p) in self.packets:
            for index, n in enumerate(range(offset - 1, offset - 1 + len(p))):
                data[n] = p[index]
        self.write(data)
        self.packets = []

    def write(self, data):
        print(data)
        size = len(data) + 1
        packet = [Dmx.START_MSG, Dmx.LABEL, size & 255, (size >> 8) & 255, Dmx.START]
        packet += data
        packet.append(Dmx.END_MSG)
        print(packet)
        packet = map(chr, packet)
        self.connection.write(''.join(packet))
        import time
        time.sleep(1/60.)

    def clear(self):
        self.write([0] * 512)

    def close(self):
        self.connection.close()
