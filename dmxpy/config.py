from dmxfixture import DMXFixture
from dmx import Dmx

from ConfigParser import ConfigParser
import colorsys
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

def create_hue(what):
    h = (what % 360) / 360.0
    s = 1
    v = 1
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))

data = dict([('intensity', 100), ('speed', 0xff), ('red', 0x0), ('blue', 0x0), ('green', 0xff)])
iteration = 0
while True:
    for df in dmxfixtures:
        extra = [0 for _ in range(df.channel_offset - 1)]
        (r, g, b) = create_hue(iteration)
        data['red'] = r
        data['green'] = g
        data['blue'] = b
        d = df.create_packet(data)
        dmx.write(extra + d)
        iteration += 1
