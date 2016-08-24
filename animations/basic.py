from bibliopixel import LEDStrip
import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim

import math
import time
import random
from audioop import rms
import pyaudio

class ColorFade(BaseStripAnim):
    def __init__(self, hue, led, start=0, end=-1):
        super(ColorFade, self).__init__(led, start, end)
        self.hue = hue

    def step(self, amt = 1):
        p = (50+20*math.cos(self._step/100.))/100
        s = int(p*255)
        c = (self.hue,s, 100)
        self._led.fillHSV(c)
        self._step += amt
