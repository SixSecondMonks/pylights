from bibliopixel import LEDStrip
import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim

import math
import time
import random
from audioop import rms
import pyaudio

class RainbowCycle(BaseStripAnim):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=-1):
        super(RainbowCycle, self).__init__(led, start, end)
        print(self._size)
#        self.frames = [[colors.hue_helper(c, self._size, i) for c in range(self._size)] for i in range(255)]
        frames = [    list(sum([colors.hue_helper(c, self._size, i) for c in range(self._size)], ()))     for i in range(255)]
        self.frames = map(lambda x: colors.color_scale(x, 175), frames)

    def step(self, amt = 1):
#        print(self._step, self._step % 255)
        self._led.setBuffer(self.frames[self._step % 255])

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow
