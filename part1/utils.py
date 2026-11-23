import datasets
from datasets import load_dataset
from transformers import AutoTokenizer
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification
from torch.optim import AdamW
from transformers import get_scheduler
import torch
from tqdm.auto import tqdm
import evaluate
import random
import argparse
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer

random.seed(0)


def example_transform(example):
    example["text"] = example["text"].lower()
    return example


### Rough guidelines --- typos
# For typos, you can try to simulate nearest keys on the QWERTY keyboard for some of the letter (e.g. vowels)
# You can randomly select each word with some fixed probability, and replace random letters in that word with one of the
# nearest keys on the keyboard. You can vary the random probablity or which letters to use to achieve the desired accuracy.


### Rough guidelines --- synonym replacement
# For synonyms, use can rely on wordnet (already imported here). Wordnet (https://www.nltk.org/howto/wordnet.html) includes
# something called synsets (which stands for synonymous words) and for each of them, lemmas() should give you a possible synonym word.
# You can randomly select each word with some fixed probability to replace by a synonym.


# Tunable: raise these if accuracy drop on transformed test is <= 4 points.
WORD_TYPO_PROB = 0.4
CHAR_TYPO_PROB = 0.35
MIN_WORD_LEN = 3

# QWERTY adjacent keys (lowercase). Used to simulate realistic typing mistakes.
QWERTY_NEIGHBORS = {
    "q": "wa",
    "w": "qeas",
    "e": "wrsd",
    "r": "etdf",
    "t": "ryfg",
    "y": "tugh",
    "u": "yihj",
    "i": "uojk",
    "o": "ipkl",
    "p": "ol",
    "a": "qwsz",
    "s": "awedxz",
    "d": "serfcx",
    "f": "drtgvc",
    "g": "ftyhbv",
    "h": "gyujnb",
    "j": "huiknm",
    "k": "jiolm",
    "l": "kop",
    "z": "asx",
    "x": "zsdc",
    "c": "xdfv",
    "v": "cfgb",
    "b": "vghn",
    "n": "bhjm",
    "m": "njk",
}


def _introduce_typos(word):
    """Replace some letters in a word with QWERTY neighbors."""
    chars = list(word)
    for i, ch in enumerate(chars):
        lower = ch.lower()
        if lower not in QWERTY_NEIGHBORS:
            continue
        if random.random() >= CHAR_TYPO_PROB:
            continue
        replacement = random.choice(QWERTY_NEIGHBORS[lower])
        chars[i] = replacement.upper() if ch.isupper() else replacement
    return "".join(chars)


def custom_transform(example):
    ################################
    ##### YOUR CODE BEGINGS HERE ###

    # Design and implement the transformation as mentioned in pdf
    # You are free to implement any transformation but the comments at the top roughly describe
    # how you could implement two of them --- synonym replacement and typos.

    # You should update example["text"] using your transformation

    tokens = word_tokenize(example["text"])
    transformed = []
    for tok in tokens:
        if (
            len(tok) >= MIN_WORD_LEN
            and tok.isalpha()
            and random.random() < WORD_TYPO_PROB
        ):
            transformed.append(_introduce_typos(tok))
        else:
            transformed.append(tok)

    example["text"] = TreebankWordDetokenizer().detokenize(transformed)

    ##### YOUR CODE ENDS HERE ######

    return example
