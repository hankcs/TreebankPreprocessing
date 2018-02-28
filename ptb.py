# -*- coding:utf-8 -*-
# Filename: make_ptb.py
# Author：hankcs
# Date: 2017-11-02 23:42
import argparse
from os.path import join

from utility import combine_files, make_sure_path_exists, eprint


def combine(folder_ids, out_path, task):
    print('Generating: ' + out_path)
    print('Section(s): ' + folder_ids.__str__())
    with open(out_path, 'w') as out:
        fids = []
        for fid in folder_ids:
            for file in ptb.fileids():
                if file.startswith('WSJ/%02d/' % fid):
                    # print(file)
                    fids.append(file)

        combine_files(fids, out, ptb, task)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine Penn Treebank WSJ MRG files into train/dev/test set')
    parser.add_argument("--output", required=True, dest="output",
                        help='The folder where to store the output train/dev/test files')
    parser.add_argument("--task", dest="task", default='par',
                        help='Which task (par, pos)? Use par for phrase structure parsing, pos for part-of-speech '
                             'tagging')

    args = parser.parse_args()
    root_path = args.output
    task = args.task
    ext = 'txt'

    if task == 'par':
        training = list(range(2, 21 + 1))
        development = [22]
        test = [23]
    elif task == 'pos':
        training = list(range(0, 18 + 1))
        development = list(range(19, 21 + 1))
        test = list(range(22, 24 + 1))
        ext = 'tsv'
    else:
        eprint('Invalid task {}'.format(task))
        exit(1)

    print('Importing ptb from nltk')
    from nltk.corpus import ptb

    print()

    make_sure_path_exists(root_path)
    combine(training, join(root_path, 'train.{}'.format(ext)), task)
    combine(development, join(root_path, 'dev.{}'.format(ext)), task)
    combine(test, join(root_path, 'test.{}'.format(ext)), task)
