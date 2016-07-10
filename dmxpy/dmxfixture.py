
class DMXFixture:
    def __init__(self, **kwargs):
        self.number_channels = int(kwargs.pop('number_channels')) # required
        self.channel_offset = int(kwargs.pop('channel_offset')) # required
        self.is_dmx = bool(kwargs.pop('real', False)) # required
        self.config = kwargs

    def create_packet(self, attrs):
        init = [0 for i in range(self.number_channels)]
        if self.is_dmx:
            for (attr, val) in attrs.items():
                if attr in self.config:
                    key = int(self.config[attr])
                    if key < len(init):
                        init[key] = val
        else:
            # TODO we assume rgb here
            for i in range(self.number_channels / 3):
                init[i*3 + 0] = attrs['red']
                init[i*3 + 1] = attrs['green']
                init[i*3 + 2] = attrs['blue']
        return init

if __name__ == '__main__':
    f = DMXFixture(**{'number_channels': 10, 'red': 5, 'green': 6, 'blue': 7})
    data = [('red', 0xff), ('blue', 0x3f), ('green', 0x7f)]
    print(f.create_packet(data))
