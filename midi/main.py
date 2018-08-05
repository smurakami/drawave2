import time
import rtmidi2

import requests

import subprocess

import numpy as np
from pydub import AudioSegment
import array

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
    pass
    # raise(IOError("Input port not found."))


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


file_to_play = '../data/solo_sounds/cat.mp3'


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


def mix(file_a, file_b, rate_a, rate_b, wav_output):
    segment_a = AudioSegment.from_mp3(file_a)
    segment_b = AudioSegment.from_mp3(file_b)

    array_a = segment_a.get_array_of_samples()
    array_b = segment_b.get_array_of_samples()

    a = np.array(array_a)
    b = np.array(array_b)

    mixed = (a * rate_a + b * rate_b).astype(a.dtype)
    mixed = array.array(segment_a.array_type, mixed)

    segment_mix = segment_a._spawn(mixed)
    segment_mix.export(wav_output, format="wav")
    return 



def interpolate(origin_file_index, target):
    target = target.reshape((-1, ))
    feat = embedding_interp.reshape((len(embedding_interp), -1))

    origin = feat[origin_file_index]
    # target = feat[origin_file_index] + np.random.random(origin.shape) * 0.1
    # target = feat[1]
    delta = origin - target
    deltas = feat - target

    cossim = np.matmul(delta, deltas.T) / (np.linalg.norm(delta) * np.linalg.norm(deltas, axis=1))
    cand = np.arange(len(cossim))[(cossim < -0.8) & (np.isnan(cossim) == False)]

    if len(cand) == 0:
        return None, 0

    cand_feat = feat[cand]
    cand_deltas = deltas[cand]

    dest_index = np.argsort(np.linalg.norm(cand_deltas, axis=1))[0]
    dest_feat = cand_feat[dest_index]

    origin_dist = np.linalg.norm(target - origin)
    dest_dist = np.linalg.norm(target - dest_feat)

    origin_rate = dest_dist / (origin_dist + dest_dist)
    dest_rate = origin_dist / (origin_dist + dest_dist)

    dest_file_index = cand[dest_index]

    return dest_file_index, dest_rate


timestamp = 0

while True:
    try:
        data = requests.get('http://smurakami.com:8888/data/timestamp.json').json()
        timestamp_ = data['timestamp']

        if timestamp != timestamp_:

            paths = requests.get('http://smurakami.com:8888/data/paths.json').json()

            print('update ditected')

            params = predict(paths)
            params = params.reshape((12, 1, 1))

            draw_embedding = (params * class_embedding).sum(axis=0)[None, :, :]

            dist = np.sqrt(((embedding_interp - draw_embedding) ** 2).sum(axis=2).sum(axis=1))

            origin_file_index = np.argmin(dist)
            print(origin_file_index)


            dest_file_index, dest_rate = interpolate(origin_file_index, draw_embedding)

            if dest_file_index is not None:
                print('interpolate!')
                mix('../sounds/' + files_interp[origin_file_index], "../sounds/" + files_interp[dest_file_index], 1 - dest_rate, dest_rate, './output.wav')
                file_to_play = './output.wav'
            else:
                file_to_play = '../sounds/' + files_interp[origin_file_index]

            subprocess.Popen([
                'play',
                file_to_play])


            timestamp = timestamp_
    except:
        import traceback
        print(traceback.format_exc())
        print('some error request')

    time.sleep(0.5)

    # message = input_port.get_message()
    # if message: print(message)


