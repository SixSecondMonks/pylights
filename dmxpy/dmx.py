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
        if tcp_port is None:
            self.connection = DmxSerial(destination)
        else:
            self.connection = DmxTcp(destination, tcp_port)

    def write(self, data):
        size = len(data) + 1
        packet = [Dmx.START_MSG, Dmx.LABEL, size & 255, (size >> 8) & 255, Dmx.START]
        packet += data
        packet.append(Dmx.END_MSG)
        packet = map(chr, packet)
        self.connection.write(''.join(packet))

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
        self.write([0] * 512)

    def close(self):
        self.connection.close()
