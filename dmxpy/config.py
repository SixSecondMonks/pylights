from ConfigParser import ConfigParser
from dmxfixture import DMXFixture
import sys

def read_config(args):

    if len(args) != 2:
        print('Usage: ', args[0], '<config file>')
        sys.exit(1)

    config = ConfigParser()
    config.readfp(open(args[1]))

    dmxfixtures = []
    for section in config.sections():
        if section == 'devices':
            continue
        dmxconfig = dict(config.items(section))
        dmxfixture = DMXFixture(**dmxconfig)
        dmxfixtures.append(dmxfixture)

    return dmxfixtures
