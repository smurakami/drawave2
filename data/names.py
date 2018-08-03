import glob
import json
from pathlib import Path
import os


pwd = Path(__file__).parent


def main():
    xs, ys = json.load(open('names.json'))
    for x in xs:
        folder = x['folder']

        print(folder)


    print()
    for y in ys:
        folder = y['folder']

        print(folder)





    # print(a)


main()

