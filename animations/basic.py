from bibliopixel import LEDStrip
import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim

import math
import time
import random
from audioop import rms
import pyaudio

class ColorFill(BaseStripAnim):
    def __init__(self, led, r, g, b, start=0, end=-1):
        super(ColorFill, self).__init__(led, start, end)
        self.rgb = (r, g, b)

    def step(self, amt = 1):
        r, g, b = self.rgb
        fade = 77
        r, g, b = fade, fade, fade
        self._led.fillRGB(r, g, b)
        self._step += amt

class ColorFade(BaseStripAnim):
    def __init__(self, hue, led, start=0, end=-1):
        super(ColorFade, self).__init__(led, start, end)
        self.hue = hue

    def step(self, amt = 1):
        saturation = int(50 * math.cos(self._step / 50.) + 80)
        c = (self.hue, saturation, 100)
        self._led.fillHSV(c)
        self._step += amt

class RotatingColors(BaseStripAnim):
    def __init__(self, bounds, led, start=0, end=-1):
        super(RotatingColors, self).__init__(led, start, end)
        self.bounds = bounds
        names = filter(lambda x: "White" not in x and isinstance(getattr(colors, x), tuple), dir(colors))
        self.colors = map(lambda c: colors.color_scale(getattr(colors, c), 64), names)
        self.n = 0

    def step(self, amt = 1):
        # We have self.bounds which is really just an array of lengths of each individual stuff, in order
        # ex: [50, 169, 100, 169, 50]

	total = sum(self.bounds)
        print self._step
        pos = 0
        for i in range(len(self.bounds)):
            for j in range(self.bounds[i]):
                (r,g,b) = self.colors[self.n % len(self.colors)]
                self._led.setRGB(pos, r, g, b)
                pos += 1
            self.n = (self.n + 1) % total

        self.n -= len(self.bounds) - 1
        self._step += amt

class Snake(BaseStripAnim):
    def __init__(self, led, start=0, end=-1):
        super(Snake, self).__init__(led, start, end)
        self.initialized = False
        self.direction = 0

    def step(self, amt = 1):
        if not self.initialized:
            self._led.fillHSV((0, 255, 255))
            self.initialized = True
        else:
            if self.direction == 0:
                self._led.setHSV(self._step, (128, 255, 255))
                self._step += amt
            else:
                self._led.setHSV(self._step, (0, 255, 255))
                self._step -= amt

            # 0 1 2 ... 168
            if self._step == self._size:
                self._step = self._size - 1
                self.direction = 1
            elif self._step == -1:
                self._step = 0
                self.direction = 0
