from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE
from bibliopixel import LEDStrip
from drivers import DriverDmx
from Rainbows import RainbowCycle
from fixtures import DmxFixture
f = [DmxFixture(**{'channels':8, 'offset':1, 'intensity':3, 'red':4, 'green':5, 'blue':6}), DmxFixture(**{'channels':4, 'offset':30, 'intensity':0, 'red':1, 'green':2, 'blue':3})]
driver = DriverDmx(f)
#driver2 = DriverSerial(type=LEDTYPE.WS2812B, num=100, dev='/dev/cu.usbmodem23451')
led = LEDStrip([driver])
anim = RainbowCycle(led)
anim.run(fps=240)
#anim.run()

