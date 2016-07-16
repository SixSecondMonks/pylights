class DmxFixture:
    def __init__(self, **kwargs):
        self.channels = int(kwargs.pop('channels')) #required
        self.offset   = int(kwargs.pop('offset')) #required
        self.config   = kwargs

    def create_packet(self, attrs):
        packet = [0] * self.channels

        for (attr, val) in attrs.items():
            if attr in self.config:
                key = int(self.config[attr])
                if key < len(packet):
                    packet[key] = val

        return packet

if __name__ == '__main__':
    f = DmxFixture(**{'channels': 8, 'offset': 17, 'red': 5, 'green': 6, 'blue': 7})
    data = {'red': 0xff, 'blue': 0x3f, 'green': 0x7f}
    print(f.create_packet(data)) 
