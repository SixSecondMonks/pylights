from __future__ import print_function
from ConfigParser import ConfigParser
from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE
from bibliopixel import LEDStrip
from drivers.fixtures import DmxFixture
from drivers.dmx import DriverDmx

import sys, itertools

class Program(object):
    def __init__(self, name='test'):
        self.name = name
        self.run()

    @staticmethod
    def read_config(args):
        if len(args) != 2:
            print('Usage: ', args[0], '<config file>')
            sys.exit(1)

        config = ConfigParser()
        config.readfp(open(args[1]))
        drivers = []

        def universes(section):
            d = dict(config.items(section))
            return (d['driver'], d['port'])

        for (driver, port), lights in itertools.groupby(config.sections(), universes):
            if driver == 'dmx':
                fixtures = []
                for light in list(lights):
                    l = dict(config.items(light))
                    fixtures.append(DmxFixture(**l))
                try:
                    d = DriverDmx(fixtures, port=port)
                    drivers.append(d)
                except:
                    print("not adding", port)
            elif driver == 'allpixel':
                light = dict(config.items(list(lights)[0]))
                try:
                    d = DriverSerial(num=int(light['length']),type=getattr(LEDTYPE, light['type']), dev=port)
                    drivers.append(d)
                except:
                    print("not adding", port)

        return drivers

    def get_animation(self, led):
        pass

    def run(self):
        drivers = self.read_config(sys.argv)
        if len(drivers) == 0:
            print("lol, bye")
            sys.exit(0)
        led = LEDStrip(drivers)
        anim = self.get_animation(led)
        try:
            anim.run(fps=60)
        except KeyboardInterrupt:
            print(self.name, 'terminated')

