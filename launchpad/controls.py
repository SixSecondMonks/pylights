
import mido
from string import ascii_lowercase

print('starting up launchpad controls')
print(mido.get_output_names())

portmidi = mido.Backend('mido.backends.portmidi')
input = portmidi.open_input('Launchpad S MIDI 1')

def process_control(message):

    if message.value is 127:
        return {} # keydown, we don't care about these

    mapping = {
        104: 'up',
        105: 'down',
        106: 'left',
        107: 'right',
        108: 'session',
        109: 'user 1',
        110: 'user 2',
        111: 'mixer',
    }
    control = mapping[message.control]

    return { 'special' : control }

def process_button(message):
    if message.velocity is 127:
        return {} # keydown, we don't care about these

    col = message.note % 16
    row = ascii_lowercase[message.note / 16]
    coordinate = row + str(col)

    # special buttons
    special = None
    mapping = {
        8: 'vol',
        24: 'pan',
        40: 'snd A',
        56: 'snd B',
        72: 'stop',
        88: 'trk on',
        104: 'solo',
        120: 'arm'
    }
    if col is 8:
        special = mapping[message.note]
        return { 'special': special }

    return { 'coordinate': coordinate }

def keypressed(message):
    fn = process_control if message.type == 'control_change' else process_button
    return fn(message)

def loop():
    try:
        for message in input:
            translation = keypressed(message)
            if translation:
                yield translation
    except KeyboardInterrupt:
        input.close()

if __name__ == '__main__':
    try:
        for message in input:
            translation = keypressed(message)
            if translation: print(translation)

    except KeyboardInterrupt:
        input.close()
