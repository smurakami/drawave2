import rtmidi2

import time
import rtmidi2

import subprocess

midi_in = rtmidi2.MidiIn()
print(midi_in.ports)

try:
    index = midi_in.ports_matching("microKEY*")[0]
    input_port = midi_in.open_port(index)
except IndexError:
    raise(IOError("Input port not found."))


def callback(src, duration):
    kind, key, _ = src
    if kind == 144:
        print(key)
        subprocess.Popen([
            'play',
            '../data/solo_sounds/cat.mp3',
            'pitch',
            str((key - 60) * 100)
            ])


midi_in.callback = callback

while True:
    time.sleep(1.0)
    # message = input_port.get_message()
    # if message: print(message)


