"""
lettersgame.py
Author: Adam Beagle
"""
from random import choice

from .resmaps import LETTER_FREQUENCY_PATH, WORDLIST_PATH

def build_letter_frequency():
    freq_map = {}
    
    with open(LETTER_FREQUENCY_PATH) as f:
        for line in f:
            char, freq = line.split(' ')
            freq_map[char] = freq

    return freq_map

class InitError(Exception):
    pass

class WordList:
    wordlist = None

    @classmethod
    def init(cls, path):
        """
        Initialize the wordlist. Must be called before first use.
        Safe to call more than once (successive calls have no effect).
        """
        if cls.wordlist is None:
            cls.wordlist = cls._build_from_file(path)

    @classmethod
    def search(cls, word):
        """Return True if `word` is in the wordlist, otherwise False."""
        try:
            return word.upper() in cls.wordlist
        except TypeError:
            raise InitError(
                "WordList.init() must be called before search() can be used."
            )
            

    @staticmethod
    def _build_from_file(path):
        wordlist = []
        
        with open(path) as f:
            entire_file = f.read()
            wordlist = frozenset(
                word.upper() for word in entire_file.split(' ')
            )

        return wordlist
