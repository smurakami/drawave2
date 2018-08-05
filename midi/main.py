import time
import rtmidi2

import requests

import subprocess

import numpy as np

from predict import predict

midi_in = rtmidi2.MidiIn()
print(midi_in.ports)


alignment = {
    'trumpet': 'Cuba_Trumpet',
    'trombone': 'Bass_Trombone_Solo',
    'harp': 'Harp',
    'guitar': 'Suitar_Guitar',
    'violin': 'Violin_Solo',
    'cow': 'cow',
    'cat': 'cat',
    'dog': 'dog',
    'clarinet': 'Clarinet_Combi',
    'piano': 'Hammer_Dulcimer',
    'zigzag': 'thunder',
    'duck': 'goose',
}

classnames = [
    'cat',
    'clarinet',
    'cow',
    'dog',
    'duck',
    'guitar',
    'harp',
    'piano',
    'trombone',
    'trumpet',
    'violin',
    'zigzag',
]

try:
    index = midi_in.ports_matching("microKEY*")[0]
    input_port = midi_in.open_port(index)
except IndexError:
    raise(IOError("Input port not found."))


embedding_interp = np.load('../data/embedding_interp.npy')
files_interp = np.load('../data/files_interp.npy')

files = np.load('../data/files.npy')
embedding = np.load('../data/embedding.npy')


class_embedding = []

for classname in classnames:
    soundname = alignment[classname]

    embedding_index = [soundname == file.replace('../../solo_sounds/', '').replace('.mp3', '') for file in files].index(True)
    print(classname, soundname, embedding_index, files[embedding_index])
    class_embedding.append(embedding[embedding_index])


class_embedding = np.array(class_embedding)

print(class_embedding.shape)


# file_to_play = '../data/solo_sounds/cat.mp3'


def callback(src, duration):
    kind, key, _ = src
    if kind == 144:
        print(key)
        subprocess.Popen([
            'play',
            file_to_play,
            'pitch',
            str((key - 60) * 100)
            ])


midi_in.callback = callback

timestamp = 0

while True:


    data = requests.get('http://smurakami.com:8888/data/timestamp.json').json()
    timestamp_ = data['timestamp']

    if timestamp != timestamp_:


        paths = get('http://smurakami.com:8888/data/paths.json').json()


        params = predict(paths)

        draw_embedding = (params * class_embedding).sum(axis=0)[None, :, :]

        dist = np.sqrt(((embedding_interp - draw_embedding) ** 2).sum(axis=2).sum(axis=1))

        index = np.argmin(dist)
        print(index)

        file_to_play = '../sounds/' + files_interp[index]

        time.sleep(0.5)

    # message = input_port.get_message()
    # if message: print(message)


