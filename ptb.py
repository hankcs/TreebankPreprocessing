# -*- coding:utf-8 -*-
# Filename: make_ptb.py
# Author：hankcs
# Date: 2017-11-02 23:42
import argparse
from os.path import join

from utility import combine_files


def combine(folder_ids, out_path):
    print('Generating ' + out_path)
    with open(out_path, 'w') as out:
        fids = []
        for fid in folder_ids:
            for file in ptb.fileids():
                if file.startswith('WSJ/%02d/' % fid):
                    # print(file)
                    fids.append(file)

        combine_files(fids, out, ptb)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine Penn Treebank WSJ MRG files into train/dev/test set')
    parser.add_argument("--output", required=True, dest="output",
                        help='The folder where to store the output train.txt/dev.txt/test.txt')

    args = parser.parse_args()
    training = list(range(2, 21 + 1))
    development = [22]
    test = [23]
    root_path = args.output
    print('Importing ptb from nltk')
    from nltk.corpus import ptb
    print()

    combine(training, join(root_path, 'train.txt'))
    combine(development, join(root_path, 'dev.txt'))
    combine(test, join(root_path, 'test.txt'))
