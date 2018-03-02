# -*- coding:utf-8 -*-
# Filename: ptb-to-stanford.py
# Author：hankcs
# Date: 2017-11-22 12:26

import argparse
import tempfile
from os import system, remove, path
from os.path import join

from utility import make_sure_path_exists


def convert(src, dst, lang):
    if path.isfile(dst):
        remove(dst)
    java = 'edu.stanford.nlp.trees.EnglishGrammaticalStructure' if lang == 'en' \
        else 'edu.stanford.nlp.trees.international.pennchinese.ChineseGrammaticalStructure'
    print('Generating {}...'.format(dst))
    with open(src) as src:
        lines = src.readlines()
        for n, line in enumerate(lines):
            if n % 10 == 0 or n == len(lines) - 1:
                print("%c%.2f%%" % (13, (n + 1) / float(len(lines)) * 100), end='')
            if len(line.strip()) == 0:
                continue
            file = tempfile.NamedTemporaryFile()
            tmp = file.name
            with open(tmp, 'w') as out:
                out.write(line)
            system(
                'java -cp "*" -mx1g {} -basic -keepPunct -conllx '
                '-treeFile "{}" >> "{}"'.format(java,
                                                tmp, dst))
            # print(line)
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert combined Penn Treebank files (.txt) to Stanford Dependency format (.conllx)')
    parser.add_argument("--input", required=True,
                        help='The folder containing train.txt/dev.txt/test.txt in bracketed format')
    parser.add_argument("--lang", required=True, help='Which language? Use en for English, cn for Chinese')
    parser.add_argument("--output", required=True, dest="output",
                        help='The folder where to store the output train.conllx/dev.conllx/test.conllx in Stanford '
                             'Dependency format')

    args = parser.parse_args()
    make_sure_path_exists(args.output)
    for f in ['train', 'dev', 'test']:
        convert(join(args.input, f + '.txt'), join(args.output, f + '.conllx'), args.lang)
