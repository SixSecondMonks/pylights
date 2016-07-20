from __future__ import print_function
from bibliopixel.drivers.driver_base import DriverBase
import serial, sys
from fixtures import DmxFixture

# DMX Universe driver
class DriverDmx(DriverBase):
    START_MSG = 0x7E
    LABEL     = 0x06
    START     = 0x00
    END_MSG   = 0xE7

    def __init__(self, fixtures, port='/dev/ttyUSB0'):
        super(DriverDmx, self).__init__(num=len(fixtures))
        self.fixtures = fixtures
        self.port = port
        self.intensity = 0x0
        self.device = serial.Serial(port, baudrate=115200, timeout=1)

    @staticmethod
    def packetize(data):
        size = len(data) + 1
        packet = [DriverDmx.START_MSG, DriverDmx.LABEL, size & 255, (size >> 8) & 255, DriverDmx.START]
        packet += data
        packet.append(DriverDmx.END_MSG)
        packet = map(chr, packet)
        return packet
        
    def update(self, data):
        self._fixData(data)
        maxsize = max(map(lambda fixture: fixture.offset + fixture.channels, self.fixtures))
        data = [0 for _ in range(maxsize)]
        for i in range(len(self.fixtures)):
            offset = self.fixtures[i].offset
            packet = self.fixtures[i].create_packet({'intensity':self.intensity, 'speed':0xff, 'red':self._buf[i * 3 + 0], 'green':self._buf[i * 3 + 1], 'blue': self._buf[i * 3 + 2]})
            
            for index, n in enumerate(range(offset - 1, offset - 1 + len(packet))):
                data[n] = packet[index]

        packet = DriverDmx.packetize(data)
        self.device.write(''.join(packet))

    def setMasterBrightness(self, brightness):
        self.intensity = brightness & 0xff


