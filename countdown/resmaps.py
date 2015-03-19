"""
resmaps.py
Author: Adam Beagle

PURPOSE:
  Contains paths to resource files.
"""
from os.path import abspath, join, normpath, pardir

ROOT_PATH = normpath(join(abspath(__file__), pardir, pardir))

LETTER_FREQUENCY_PATH = join(ROOT_PATH, 'res', 'letter_frequency.txt')
WORDLIST_PATH = join(ROOT_PATH, 'res', 'wordlist.txt')
