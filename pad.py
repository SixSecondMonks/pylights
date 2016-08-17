from launchpad import controls
import os
import imp
from string import ascii_lowercase

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
    return imported_mode.run

mode_map = dict([(coord(i), run_mode(m)) for i, m in enumerate(modes)])
print(mode_map)

for pressed in controls.loop():
    print('pressed', pressed)
    if pressed['coordinate'] and pressed['coordinate'] in mode_map.keys():
        mode_map[pressed['coordinate']]()
