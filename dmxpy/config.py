from pixelpusher import PixelPusher
from dmxfixture import DMXFixture
from dmx import Dmx
from rainbow import Rainbow

from ConfigParser import ConfigParser
import sys

if len(sys.argv) != 2:
    print('Usage: ', sys.argv[0], '<config file>')
    sys.exit(1)

config = ConfigParser()
config.readfp(open(sys.argv[1]))

dmx = Dmx()
pixelpusher = PixelPusher(number=50)

dmxfixtures = []
for section in config.sections():
    if section == 'devices':
        continue
    dmxconfig = dict(config.items(section))
    dmxfixture = DMXFixture(**dmxconfig)
    dmxfixtures.append(dmxfixture)

program = Rainbow()

try:
    while True:
        for df in dmxfixtures:
            data = program.iterative_data()
            packet = df.create_packet(data)
            if df.is_dmx:
                extra = [0 for _ in range(df.channel_offset - 1)]
                dmx.write(extra + packet)
            else:
                pixelpusher.write_dmx(packet)
except KeyboardInterrupt:
    pass
