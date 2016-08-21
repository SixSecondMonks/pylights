from launchpad import controls
import os
from multiprocessing import Process, Queue
import imp
from string import ascii_lowercase
from time import sleep

# list modes
modelisting = os.walk('modes/').next()[2]
modes = [mode for mode in modelisting if mode.startswith('mode') and mode.endswith('.py')]
print('found modes', modes)

def coord(index):
    column = index % 8
    row_index = index / 8
    row = ascii_lowercase[row_index]
    return row + str(column)

def run_mode(m):
    name = m.replace('.py', '')
    imported_mode = imp.load_source(name, 'modes/' + m)
    return imported_mode

mode_map = dict([(coord(i), run_mode(m)) for i, m in enumerate(modes)])

for (k,v) in mode_map.iteritems():
    print k, "will run", v.__name__

p = None # no current process

for pressed in controls.loop():
    print('pressed', pressed)
    if pressed['coordinate'] and pressed['coordinate'] in mode_map.keys():
        if p is not None:
            p.terminate()
            sleep(1)

        mode = mode_map[pressed['coordinate']]
        p = Process(target=mode.run)
        p.start()
