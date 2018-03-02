# TreebankPreprocessing
Python scripts preprocessing [Penn Treebank (PTB)](https://catalog.ldc.upenn.edu/ldc99t42) and [Chinese Treebank 5.1 (CTB)](https://catalog.ldc.upenn.edu/LDC2005T01). They can convert treebanks to:

| Corpus | Format | Description |
| --- | --- | --- |
| constituency parse tree | `.txt` | one line for one sentence |
| dependency parse tree | `.conllx` | [Basic Stanford Dependencies (SD)](https://nlp.stanford.edu/software/stanford-dependencies.shtml) |
| part-of-speech tagging corpus | `.tsv` | first column for words, second column for tags, sentences separated by a blank line |

 
When designing a tagger or parser, preprocessing treebanks is a troublesome problem. We need to:
 
- Split dataset into train/dev/test, following conventional splits.
- Remove xml tags inside CTB.
- Combine the multiline bracketed files into one file, one line for one sentence.

I wondered why there were no open-source tools handling these tedious works. Finally I decide to write one myself. Hopefully it will save you some time.

### Required software

- Python3
- NLTK
- Optional stanford-parser for converting to dependency parse trees

## Overview

What kind of task can we perform on treebanks?

### Part-Of-Speech Tagging

As per Collins (2002) and Choi (2016), splits are:

- **PTB** Training: 0-18. Development: 19-21. Test: 22-24.
 
### Phrase Structure Parsing
These scripts can also convert treebanks into the conventional data setup from Chen and Manning (2014), Dyer et al. (2015). The detailed splits are:

- **PTB** Training: 02-21. Development: 22. Test: 23.
- **CTB** Training: 001–815, 1001–1136. Development: 886–931, 1148–1151. Test: 816–885, 1137–1147.

### Dependency Parsing

You will need Stanford Parser for converting phrase structure trees to dependency parse trees. Please download the [Stanford Parser Version 3.3.0](https://nlp.stanford.edu/software/stanford-parser-full-2013-11-12.zip) and place them in this folder:

```
TreebankPreprocessing
├── ...
├── stanford-parser-3.3.0-models.jar
└── stanford-parser.jar
```
 
OK, let's do it on the fly.
 
## PTB


 
### 1. Import PTB into NLTK

Bracketed files parsing relies on NLTK. Please follow [NLTK instruction](http://www.nltk.org/howto/corpus.html#parsed-corpora), put `BROWN` and `WSJ` into `nltk_data/corpora/ptb`, e.g.

```
ptb
├── BROWN
└── WSJ
```
### 2. Run `ptb.py`

This script does all the work for you, only requires a path to store output.

```text
$ python3 ptb.py --help 
usage: ptb.py [-h] --output OUTPUT [--task TASK]

Combine Penn Treebank WSJ MRG files into train/dev/test set

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  The folder where to store the output train/dev/test files
  --task TASK      Which task (par, pos)? Use par for phrase structure
                   parsing, pos for part-of-speech tagging
```
* You will get 3 `.txt` files corresponding to train/dev/test set.
* If you want part-of-speech tagging corpora, simply append `--task pos`. This time, you get 3 `.tsv` files.
* `.txt` files can be converted to `.conllx` files by `tb_to_stanford.py`:

```
$ python3 tb_to_stanford.py --help
usage: tb_to_stanford.py [-h] --input INPUT --lang LANG --output OUTPUT

Convert combined Penn Treebank files (.txt) to Stanford Dependency format
(.conllx)

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT    The folder containing train.txt/dev.txt/test.txt in
                   bracketed format
  --lang LANG      Which language? Use en for English, cn for Chinese
  --output OUTPUT  The folder where to store the output
                   train.conllx/dev.conllx/test.conllx in Stanford Dependency
                   format
```

## CTB

The CTB is a little messy, it contains extra xml tags in every gold tree, and is not natively supported by NLTK. You need to specify the CTB root path (the folder containing index.html).

```
$ python3 ctb.py --help           
usage: ctb.py [-h] --ctb CTB --output OUTPUT [--task TASK]

Combine Chinese Treebank 5.1 fid files into train/dev/test set

optional arguments:
  -h, --help       show this help message and exit
  --ctb CTB        The root path to Chinese Treebank 5.1
  --output OUTPUT  The folder where to store the output
                   train.txt/dev.txt/test.txt
  --task TASK      Which task (par, pos)? Use par for phrase structure
                   parsing, pos for part-of-speech tagging
```

- Then pos and dependency parsing corpora can be converted similar to PTB.

Then you can start your research, enjoy it!


