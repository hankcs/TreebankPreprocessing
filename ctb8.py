# -*- coding:utf-8 -*-
# Filename: make_ctb.py
# Author：hankcs
import argparse
from os import listdir
from os.path import isfile, join, isdir

import nltk

from utility import make_sure_path_exists, eprint, combine_files


def convert_ctb8_to_bracketed(ctb_root, out_root):
    ctb_root = join(ctb_root, 'bracketed')
    chtbs = [f for f in listdir(ctb_root) if isfile(join(ctb_root, f)) and f.startswith('chtb')]
    make_sure_path_exists(out_root)
    for f in chtbs:
        with open(join(ctb_root, f), encoding='utf-8') as src, open(join(out_root, f + '.txt'), 'w') as out:
            for line in src:
                if not line.startswith('<'):
                    out.write(line)


def split(ctb_root):
    chtbs = [f for f in listdir(ctb_root) if isfile(join(ctb_root, f)) and f.startswith('chtb')]
    folder = {}
    for f in chtbs:
        tag = f[-6:-4]
        if tag not in folder:
            folder[tag] = []
        folder[tag].append(f)
    train, dev, test = [], [], []
    for tag, files in folder.items():
        t = int(len(files) * .8)
        d = int(len(files) * .9)
        train += files[:t]
        dev += files[t:d]
        test += files[d:]
    return train, dev, test


def combine_fids(fids, out_path, task):
    print('Generating ' + out_path)
    files = []
    for f in fids:
        if isfile(join(ctb_in_nltk, f)):
            files.append(f)
    with open(out_path, 'w') as out:
        combine_files(files, out, ctb, task, add_s=True)


def find_nltk_data():
    global ctb_in_nltk
    for root in nltk.data.path:
        if isdir(root):
            ctb_in_nltk = root


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine Chinese Treebank 8 bracketed files into train/dev/test set')
    parser.add_argument("--ctb", required=True,
                        help='The root path to Chinese Treebank 8')
    parser.add_argument("--output", required=True,
                        help='The folder where to store the output train.txt/dev.txt/test.txt')
    parser.add_argument("--task", dest="task", default='par',
                        help='Which task (seg, pos, par)? Use seg for word segmentation, pos for part-of-speech '
                             'tagging (pos-pku for PKU format, otherwise tsv format), par for phrase structure parsing')

    args = parser.parse_args()

    ctb_in_nltk = None
    find_nltk_data()

    if ctb_in_nltk is None:
        nltk.download('ptb')
        find_nltk_data()

    ctb_in_nltk = join(ctb_in_nltk, 'corpora')
    ctb_in_nltk = join(ctb_in_nltk, 'ctb8')

    if not isdir(ctb_in_nltk):
        print('Converting CTB: removing xml tags...')
        convert_ctb8_to_bracketed(args.ctb, ctb_in_nltk)
    print('Importing to nltk...\n')
    from nltk.corpus import BracketParseCorpusReader, LazyCorpusLoader

    ctb = LazyCorpusLoader(
        'ctb8', BracketParseCorpusReader, r'chtb_.*\.txt',
        tagset='unknown')

    training, development, test = split(ctb_in_nltk)
    task = args.task
    if task == 'par' or task == 'pos-pku':
        ext = 'txt'
    elif task == 'seg' or task == 'pos':
        ext = 'tsv'
    else:
        eprint('Invalid task {}'.format(task))
        exit(1)

    root_path = args.output
    make_sure_path_exists(root_path)
    combine_fids(training, join(root_path, 'train.{}'.format(ext)), task)
    combine_fids(development, join(root_path, 'dev.{}'.format(ext)), task)
    combine_fids(test, join(root_path, 'test.{}'.format(ext)), task)
