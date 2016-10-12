import bibliopixel.colors as colors
from mixins import StripAnim

class RainbowCycleAudio(StripAnim):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, device_index, led, start=0, end=-1):
        super(RainbowCycleAudio, self).__init__(device_index, led, start, end)

    def step(self, amt = 1):
        for i in range(self._size):
            c = colors.hue_helper(i, self._size, self._step)
            d = self.decibels
            d -= 68
            d = max(0, d)
            percentage = d / 20
            percentage = min(percentage, 1.0)
            brightness = int(round(percentage * 255))
	    final = min(max(brightness, 25), 175)
            self._led.set(self._start + i, colors.color_scale(c, final))

        self._step += amt
        overflow = self._step - 256
        if overflow >= 0:
            self._step = overflow
