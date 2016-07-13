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

dmx = Dmx("localhost", 9999)
# pixelpusher = PixelPusher(number=50)

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
                dmx.fix(df.channel_offset, packet)
            else:
                pixelpusher.write_dmx(packet)
        dmx.render()
except KeyboardInterrupt:
    print('Have a nice day, foo')
    dmx.close()
