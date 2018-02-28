# -*- coding:utf-8 -*-
# Filename: utility.py
# Author：hankcs
# Date: 2017-11-03 22:05
import errno
from os import makedirs

import sys


def make_sure_path_exists(path):
    try:
        makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def combine_files(fids, out, tb, task):
    print('%d files...' % len(fids))
    total_sentence = 0
    for n, file in enumerate(fids):
        if n % 10 == 0 or n == len(fids) - 1:
            print("%c%.2f%%" % (13, (n + 1) / float(len(fids)) * 100), end='')
        sents = tb.parsed_sents(file)
        for s in sents:
            if task == 'par':
                out.write(s.pformat(margin=sys.maxsize))
            elif task == 'pos':
                for word_tag in s.pos():
                    out.write('{}\t{}\n'.format(*word_tag))
            else:
                raise RuntimeError('Invalid task {}'.format(task))
            if n != len(fids) - 1:
                out.write('\n')
            total_sentence += 1
    print()
    print('%d sentences.' % total_sentence)
    print()
