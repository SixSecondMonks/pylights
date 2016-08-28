from __future__ import print_function
from ConfigParser import ConfigParser
from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE
from bibliopixel.drivers.visualizer import DriverVisualizer
from bibliopixel.drivers.dummy_driver import DriverDummy
from bibliopixel import LEDStrip
from drivers.fixtures import DmxFixture
from drivers.dmx import DriverDmx
import math

import sys, itertools

class Program(object):
    def __init__(self, name='test', fps=60):
        self.name = name
        self.fps = fps
        self.audio_port = None
        self.run()

    def read_config(self, args):
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
            elif driver == 'emulator':
                light = dict(config.items(list(lights)[0]))
                try:
                    num_pixels = int(math.sqrt(int(light['length'])))
                    d = DriverVisualizer(width=num_pixels, height=num_pixels)
                    drivers.append(d)
                except:
                    print("error adding visualizer")
            elif driver == 'dummy':
                light = dict(config.items(list(lights)[0]))
                print(light)
                try:
                    num_pixels = int(light['length'])
                    d = DriverDummy(num=num_pixels)
                    drivers.append(d)
                except:
                    print("error adding dummy, you dummy")
            elif driver == 'audio':
                light = dict(config.items(list(lights)[0]))
                self.audio_port = int(port)

        return drivers

    def get_animation(self, led):
        pass

    def run(self):
        drivers = self.read_config(sys.argv)
        if len(drivers) == 0:
            print("no drivers, quitting")
            sys.exit(0)
        led = LEDStrip(drivers, threadedUpdate=True)
        anim = self.get_animation(led)
        try:
            anim.run(fps=self.fps)
        except KeyboardInterrupt:
            print(self.name, 'terminated')

