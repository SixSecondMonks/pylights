from bibliopixel import LEDStrip
from DriverDmx import DriverDmx
from Rainbows import RainbowCycle
driver = DriverDmx(1)
led = LEDStrip(driver)
anim = RainbowCycle(led)
anim.run()

