"""
lettersround.py
Author: Adam Beagle
"""
from random import randrange

from .resmaps import LETTER_FREQUENCY_PATH, WORDLIST_PATH

def build_letter_frequency(path):
    """
    Return dictionary whose keys are each letter of the alphabet, and whose
    values are the number of times each letter can appear in its respective
    pile.

    'path' is assumed to point to a file with each line formatted
    [letter][one space][number]

    For example, a portion of the file may look as such:
    
    a 10
    b 5
    c 4
    """
    freq_map = {}
    
    with open(path) as f:
        for line in f:
            char, freq = line.split(' ')
            freq_map[char] = int(freq)

    return freq_map

class InitError(Exception):
    pass

class LettersRoundError(Exception):
    pass

class WordList:
    """
    Defines an object that faciliates dictionary (as in Webster's) lookups.
    Uses frozenset for O(1) lookups.

    Init expects a path to a file containing words separated by a single space
    and no newlines. The dictionary is built from all words in said file.

    METHODS:
      init   - Must call this before first use.
      search - Search for a word.
    """
    wordlist = None

    @classmethod
    def init(cls, path):
        """
        Initialize the wordlist. Must be called before first use.
        Safe to call more than once (successive calls have no effect).

        'path' is assumed to point to a file containing words separated by a
        single space and no newlines. The dictionary is built from all words
        in said file.
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

class LettersRound:
    """
    All public methods return (success code, message) where `success code`
    is a boolean representing general success or failure of a given operation,
    and `message` provides more information to the user, if applicable (message
    can be empty).
    
    METHODS:
      add_consonant
      add_vowel
      verify_word
    """
    wordlist = WordList()
    letter_frequency = build_letter_frequency(LETTER_FREQUENCY_PATH)
    max_letters = 9

    min_vowels = 3
    min_consonants = 4
    
    max_consonants = max_letters - min_vowels
    max_vowels = max_letters - min_consonants
    
    def __init__(self):
        self.wordlist.init(WORDLIST_PATH)
        self.consonants, self.vowels = self._init_letter_bags()
        self.showing = []
        self.num_consonants = 0
        self.num_vowels = 0

    def add_consonant(self):
        if self.num_consonants < self.max_consonants:
            i = randrange(len(self.consonants))
            self._add_to_showing(self.consonants.pop(i))
            self.num_consonants += 1
            
            return True, ''

        return False, 'Minimum {} vowels required'.format(self.min_vowels)

    def add_vowel(self):
        if self.num_vowels < self.max_vowels:
            i = randrange(len(self.vowels))
            self._add_to_showing(self.vowels.pop(i))
            self.num_vowels += 1
            
            return True, ''

        return False, 'Minimum {} consonants required'.format(
            self.min_consonants
        )
    
    def verify_word(self, word):
        word = word.upper()
        remaining = self.showing[:]

        # Verify word can be made from available letters
        for letter in word:
            if letter in remaining:
                remaining.remove(letter)
            else:
                return False, 'Sorry, word cannot be made from given letters.'

        # Verify word in dictionary
        if self.wordlist.search(word):
            return True, "Word is valid!"
        else:
            return False, "Sorry, your word was not found in the dictionary."

    def _add_to_showing(self, letter):
        if self.showing_full:
            raise LettersRoundError(
                "max_letters reached. Cannot add another letter."
            )

        self.showing.append(letter)

    def _init_letter_bags(self):
        freq = self.letter_frequency
        vowels = []
        consonants = []
        
        for letter in freq:
            if letter in ('A', 'E', 'I', 'O', 'U'):
                vowels += freq[letter]*[letter]
            else:
                consonants += freq[letter]*[letter]

        return consonants, vowels

    @property
    def showing_full(self):
        return len(self.showing) == self.max_letters
