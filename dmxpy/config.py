from dmxfixture import DMXFixture
from dmx import Dmx
from rainbow import Rainbow

from ConfigParser import ConfigParser
import sys

if len(sys.argv) != 2:
    print('Usage: ', sys.argv[0], '<config file>')
    sys.exit(1)

dmxfixtures = []
dmx = Dmx()

config = ConfigParser()
config.readfp(open(sys.argv[1]))
for section in config.sections():
    dmxconfig = dict(config.items(section))
    dmxfixture = DMXFixture(**dmxconfig)
    dmxfixtures.append(dmxfixture)

program = Rainbow()

while True:
    for df in dmxfixtures:
        extra = [0 for _ in range(df.channel_offset - 1)]
        data = program.iterative_data()
        packet = df.create_packet(data)
        dmx.write(extra + packet)
