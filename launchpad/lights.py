
import mido
from string import ascii_lowercase

print('starting up launchpad controls')
print(mido.get_output_names())

portmidi = mido.Backend('mido.backends.portmidi')
output = portmidi.open_output('Launchpad S MIDI 1')

colors = {
    'off': 0,
    'red.low': 1,
    'red.medium': 2,
    'red.high': 3,
    'yellow.low': 17,
    'yellow.medium': 34,
    'yellow.high': 54,
    'orange.low': 45,
    'orange.medium': 46,
    'orange.high': 23,
    'green.low': 16,
    'green.medium': 32,
    'green.high': 48
}

def setlight(where, what):
    if not 'coordinate' in where:
        # ignore if it is not on the board
        return
    coord = where['coordinate']
    x = ascii_lowercase.index(coord[0])
    y = int(coord[1])
    note = (y * 16) + x
    color = colors[what] if what in colors else 0
    message = mido.Message('note_on', note=note, velocity=color)
    output.send(message)

# for special buttons (not implemented),
#   control_change
#   note=104 + x
#   velocity=color

if __name__ == '__main__':
    import time
    for color in sorted(colors.keys()):
        print('setting board to color', color)
        for i in range(8):
            for j in range(8):
                x = ascii_lowercase[i]
                y = str(j)
                coord = x + y
                setlight({'coordinate': coord}, color)
        time.sleep(0.5)

    # test invalid settings
    setlight({'coordinate': 'a0'}, 'asdf')
    setlight({'special': 'trk on'}, 'asdf')
