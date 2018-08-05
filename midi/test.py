from pydub import AudioSegment
import numpy as np

import array

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


def interpolate(origin_index, target):

    feat = 


    origin = feat[origin_index]
    # target = feat[origin_index] + np.random.random(origin.shape) * 0.1
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



