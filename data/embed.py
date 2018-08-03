import glob
import json
from pathlib import Path
import os
import numpy as np


pwd = Path(__file__).parent

embedding = np.load('./embedding.npy')
files = np.load('./files.npy')

names = [file.replace('../../solo_sounds/', '').replace('.mp3', '') for file in files]


def main():
    embedding_interp = []
    files_interp = []

    xs, ys = json.load(open('names.json'))
    for x in xs:
        folder_x = x['folder']
        for y in ys:
            folder_y = y['folder']

            folder = '_'.join([folder_x, folder_y])

            # print(folder)

            index_x = names.index(folder_x)
            index_y = names.index(folder_y)
            print(index_x, index_y)

            feat_x = embedding[index_x]
            feat_y = embedding[index_y]

            for i in range(5):
                file = "{}/{}_60.mp3".format(folder, i)
                embed = feat_x * i / 4 + feat_y * (4 - i) / 4
                files_interp.append(file)
                embedding_interp.append(embed)


    np.save('embedding_interp.npy', embedding_interp)
    np.save('files_interp.npy', files_interp)

            # folder_ = list((pwd / '../sounds').glob("*{}".format(folder)))[0]
            # sound = folder_ / '0_60.mp3'
            # dst = pwd / 'solo_sounds' / (str(folder) + '.mp3')
            # os.system('cp {} {}'.format(sound, dst))





    # print(a)


main()

