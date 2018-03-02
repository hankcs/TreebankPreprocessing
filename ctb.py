# -*- coding:utf-8 -*-
# Filename: make_ctb.py
# Author：hankcs
# Date: 2017-11-03 21:23
import argparse
from os import listdir
from os.path import isfile, join, isdir

import nltk

from utility import make_sure_path_exists, eprint, combine_files


def convert(ctb_root, out_root):
    ctb_root = join(ctb_root, 'bracketed')
    fids = [f for f in listdir(ctb_root) if isfile(join(ctb_root, f)) and f.endswith('.fid')]
    make_sure_path_exists(out_root)
    for f in fids:
        with open(join(ctb_root, f), encoding='GB2312') as src, open(join(out_root, f), 'w') as out:
            in_s_tag = False
            try:
                for line in src:
                    if line.startswith('<S ID='):
                        in_s_tag = True
                    elif line.startswith('</S>'):
                        in_s_tag = False
                    elif in_s_tag:
                        out.write(line)
            except:
                pass


def combine_fids(fids, out_path, task):
    print('Generating ' + out_path)
    files = []
    for fid in fids:
        f = 'chtb_%03d.fid' % fid
        if fid > 1000:
            f = 'chtb_%04d.fid' % fid
        if isfile(join(ctb_in_nltk, f)):
            files.append(f)
    with open(out_path, 'w') as out:
        combine_files(files, out, ctb, task, add_s=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine Chinese Treebank 5.1 fid files into train/dev/test set')
    parser.add_argument("--ctb", required=True,
                        help='The root path to Chinese Treebank 5.1')
    parser.add_argument("--output", required=True,
                        help='The folder where to store the output train.txt/dev.txt/test.txt')
    parser.add_argument("--task", dest="task", default='par',
                        help='Which task (par, pos)? Use par for phrase structure parsing, pos for part-of-speech '
                             'tagging')

    args = parser.parse_args()

    ctb_in_nltk = None
    for root in nltk.data.path:
        if isdir(root):
            ctb_in_nltk = root

    if ctb_in_nltk is None:
        eprint('You should run nltk.download(\'ptb\') to fetch some data first!')
        exit(1)

    ctb_in_nltk = join(ctb_in_nltk, 'corpora')
    ctb_in_nltk = join(ctb_in_nltk, 'ctb')

    print('Converting CTB: removing xml tags...')
    convert(args.ctb, ctb_in_nltk)
    print('Importing to nltk...\n')
    from nltk.corpus import BracketParseCorpusReader, LazyCorpusLoader

    ctb = LazyCorpusLoader(
        'ctb', BracketParseCorpusReader, r'chtb_.*\.fid',
        tagset='unknown')

    training = list(range(1, 815 + 1)) + list(range(1001, 1136 + 1))
    development = list(range(886, 931 + 1)) + list(range(1148, 1151 + 1))
    test = list(range(816, 885 + 1)) + list(range(1137, 1147 + 1))

    task = args.task
    if task == 'par':
        ext = 'txt'
    elif task == 'pos':
        ext = 'tsv'
    else:
        eprint('Invalid task {}'.format(task))
        exit(1)

    root_path = args.output
    combine_fids(training, join(root_path, 'train.{}'.format(ext)), task)
    combine_fids(development, join(root_path, 'dev.{}'.format(ext)), task)
    combine_fids(test, join(root_path, 'test.{}'.format(ext)), task)
