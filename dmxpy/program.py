from config import read_config
from pixelpusher import PixelPusher
from dmx import Dmx

import sys

class Program(object):
    def __init__(self):
        self.run()

    def initial_data():
        pass

    def iterative_data():
        pass

    def run(self):
        dmx = Dmx("localhost", 9999)
        # pixelpusher = PixelPusher(number=50)
        fixtures = read_config(sys.argv)
        try:
            while True:
                for df in fixtures:
                    data = self.iterative_data()
                    packet = df.create_packet(data)
                    if df.is_dmx:
                        dmx.fix(df.channel_offset, packet)
                    else:
                        pixelpusher.fix(packet)
                dmx.render()
                #pixelpusher.render()
        except KeyboardInterrupt:
            print(self.name, 'terminated')
            dmx.close()
