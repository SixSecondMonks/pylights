#  ## YellowTwinkle ##
# This Bibliopixel animation randomly picks leds and slowly brightens them to a max brightness
# then dims them to off.
#
# Author: Bob Steinbeiser, based on work by Mark Kriegsman at:
#    https://gist.github.com/kriegsman/99082f66a726bdff7776
#
#  ## Usage ##
#
#  max_led -    The max number of pixels you want used ('None' for all leds)
#  speed   -    How fast the leds bighten then dim (best in range 2-40)
#  density -    The density (or number) of twinkling leds
#  max_bright - The maximum brightness, some leds twinkle better if they ramp to less than full
#                 brightness (19 - 255). Lower brightness also speeds up the twinkle rate.

import time, random
from random import randint
from bibliopixel.animation import *

class LedColorDirection:

    def __init__(self, base_color, scale, direction):
        self.base_color = base_color
        self.scale = scale
        self.direction = direction

class YellowTwinkle(BaseStripAnim):
    """ Random white twinkling leds """

    def __init__(self, led, max_led=None, density=169, speed=1, max_bright=255):

        super(YellowTwinkle, self).__init__(led, 0, -1)
        self._current = 0
        self._minLed = 0
        self._maxLed = max_led
        if self._maxLed == None or self._maxLed < self._minLed:
            self._maxLed = self._led.lastIndex
        self.density = density
        self.speed = speed
        self.max_bright = max_bright

        self.preselectedColors = [ colors.Red, colors.Orange, colors.Yellow ]

        # dictionary to contain active pixels
        self.activeLeds = {}

        # If max_bright is even then leds won't ever dim, make it odd
        if (self.max_bright & 1 == 0):
            self.max_bright -= 1

        # If the speed is odd then the leds won't ever brighten, make it even
        if self.speed & 1:
            self.speed += 1

        # Make sure speed, density & max_bright are in sane ranges
        self.speed = min(self.speed, 100)
        self.speed = max(self.speed, 2)
        self.density = min(self.density, 169)
        self.density = max(self.density, 2)
        print("density set to", self.density)
        self.max_bright = min(self.max_bright, 255)
        self.max_bright = max(self.max_bright, 5)


    def qadd8 (self, color, inc):
        # increment the color brightness to a max of max_bright (that becomes odd)
        r = min(color[0] + inc, self.max_bright)
        g = min(color[1] + inc, self.max_bright)
        b = min(color[2] + inc, self.max_bright)
        return (r, g, b)

    def qsub8 (self, color, dec):
        # decrement the color brightness to a min of 0 (that becomes even)
        r = max(color[0] - dec, 0)
        g = max(color[1] - dec, 0)
        b = max(color[2] - dec, 0)
        return (r, g, b)

    def pick_random_base_color(self):
        # create a random base color
        r = randint(1,255)
        g = randint(1,255)
        b = randint(1,255)
        return (r,g,b)

    def pick_preselected_color(self):
        size = len(self.preselectedColors)
        return self.preselectedColors[randint(0,size-1)]

    def create_random_color_led_direction(self):
        return LedColorDirection(self.pick_random_base_color(), 5, 1)

    def create_from_preselected_colors_led_direction(self):
        return LedColorDirection(self.pick_preselected_color(), 5, 1)

    def pick_led(self, inc):
        # Pick a random led, if it's off bump it up an even number so it gets brighter
        idx =  random.randrange(0,self._led.numLEDs)
        this_led = self._led.get(idx)
        r,g,b = this_led[0], this_led[1], this_led[2]

        if len(self.activeLeds) < self.density:
            if r == 0 and g == 0 and b == 0:
                # add to active directory
                self.activeLeds[idx] = self.create_random_color_led_direction()

    def step(self, amt = 1):
        # The direction of fade is determined by the red value of the led color
        self.pick_led(self.speed)

        # make copy of keys for iterator so we dont blow ourselves up when calling .pop()
        for i in self.activeLeds.keys():

            aled = self.activeLeds[i]

            if aled.scale < 255 and aled.direction == 1:
                aled.scale = min(aled.scale + self.speed, 255)
            elif aled.direction == -1:
                aled.scale = max(aled.scale - self.speed, 0)
            elif aled.scale == 255 and aled.direction == 1:
                aled.direction = -1 

            if aled.scale == 0: 
                self._led.setOff(i)
                self.activeLeds.pop(i, None)
            else:
                self.activeLeds[i] = aled        
                self._led.set(i, colors.color_scale(aled.base_color, aled.scale))

        self._step += amt

MANIFEST = [
    {
        "class": YellowTwinkle, 
        "controller": "strip", 
        "desc": "Random White Twinkling Leds", 
        "display": "Random White Twinkling Leds", 
        "id": "WhiteTwinkle", 
        "params": [
            {
                "default": None, 
                "help": "Last pixel index to use. Leave empty to use max index.", 
                "id": "max_led", 
                "label": "Last Pixel", 
                "type": "int"
            }, 
            {
                "default": 2, 
                "help": "Fade up/down speed of the twinkle (best in range of 2-20) (100 max)", 
                "id": "speed", 
                "label": "Fade Speed", 
                "type": "int"
            }, 
            {
                "default": 80, 
                "help": "Density (or number) of the twinkling leds (best in range 40-80) (100 max)", 
                "id": "density", 
                "label": "Twinkling LED Density", 
                "type": "int"
            },
            {
                "default": 255, 
                "help": "Some leds twinkle better at less than full brightness. This also speeds up the twinkle rate. (255 max)", 
                "id": "max_bright", 
                "label": "LED Max Brightness", 
                "type": "int"
            }
        ], 
        "type": "animation"
    }
]
