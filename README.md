# TreebankPreprocessing
Python scripts preprocessing [Penn Treebank (PTB)](https://catalog.ldc.upenn.edu/ldc99t42) and [Chinese Treebank 5.1 (CTB)](https://catalog.ldc.upenn.edu/LDC2005T01). 
 
When designing a tagger or parser, preprocessing treebanks is a troublesome problem. We need to:
 
- Split dataset into train/dev/test, following conventional splits.
- Remove xml tags inside CTB.
- Combine the multiline bracketed files into one file, one line for one sentence.

I wondered why there were no open-source tools handling these tedious works. Then I decide to write one myself. Hopefully it will save you some time.

## Conventional Splits

### Part-Of-Speech Tagging

As per Collins (2002) and Choi (2016), splits are:

- **PTB** Training: 0-18. Development: 19-21. Test: 22-24.
 
### Phrase Structure Parsing
These scripts convert treebanks into the conventional data setup from Chen and Manning (2014), Dyer et al. (2015). The detailed splits are:

- **PTB** Training: 02-21. Development: 22. Test: 23.
- **CTB** Training: 001–815, 1001–1136. Development: 886–931, 1148–1151. Test: 816–885, 1137–1147.

Let's do it on the fly.

### Required software

- Python3
- NLTK
 
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
usage: ptb.py [-h] --output OUTPUT [--task TASK]

Combine Penn Treebank WSJ MRG files into train/dev/test set

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  The folder where to store the output train/dev/test files
  --task TASK      Which task (par, pos)? Use par for phrase structure
                   parsing, pos for part-of-speech tagging
```

E.g.

```
$ python3 ptb.py --output ptb-combined
Importing ptb from nltk

Generating ptb-combined/train.txt
1875 files...
100.00%
39832 sentences.

Generating ptb-combined/dev.txt
83 files...
100.00%
1700 sentences.

Generating ptb-combined/test.txt
100 files...
100.00%
2416 sentences.
```

If you want part-of-speech tagging corpora, simply append `--task pos`.

## CTB

The CTB is a little messy, it contains extra xml tags in every gold tree, and is not natively supported by NLTK. You need to specify the CTB root path (the folder containing index.html).

```
usage: ctb.py [-h] --ctb CTB --output OUTPUT

Combine Chinese Treebank 5.1 fid files into train/dev/test set

optional arguments:
  -h, --help       show this help message and exit
  --ctb CTB        The root path to Chinese Treebank 5.1
  --output OUTPUT  The folder where to store the output
                   train.txt/dev.txt/test.txt
```

E.g.

```text
$ python3 ctb.py --ctb corpus/ctb5.1 --output ctb5.1-combined
Converting CTB: removing xml tags...
Importing to nltk...

Generating ctb5.1-combined/train.txt
773 files...
100.00%
16083 sentences.

Generating ctb5.1-combined/dev.txt
36 files...
100.00%
803 sentences.

Generating ctb5.1-combined/test.txt
81 files...
100.00%
1910 sentences.
```

Then you can start your research, enjoy it!


