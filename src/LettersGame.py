"""
Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""

from random import choice
from os import path

#################################################################################################
class LettersGame(object):

    #**********************************************************
    #---------------------- CONSTRUCTOR ----------------------*
    #**********************************************************
    def __init__(self, numLetters=9):
        self._maxLen = numLetters
        self._maxConsonants = 6
        self._maxVowels = 5
        self._wordList = self._init_dictionary(path.join(path.dirname(__file__), '..', 'res', 'WordList.txt'))
        self._letterFrequency = self._init_letter_freq(path.join(path.dirname(__file__), '..', 'res', 'LetterFreq.txt'))
        self._allConsonants, self._allVowels = self._build_tiles()
        
        self.Reset()
        
    #**********************************************************
    #--------------------- PUBLIC METHODS --------------------*
    #**********************************************************
    def AddRandomConsonant(self):
        if self.NumConsonants < self._maxConsonants:
            if self._add_rand_letter(self._remConsonants):
                self._numConsonants += 1
                return True, ''
        else:
            return False, 'Minimum 3 vowels required'

    #-----------------------------------------------------------------------  
    def AddRandomVowel(self):
        if self.NumVowels < self._maxVowels:
            if self._add_rand_letter(self._remVowels):
                self._numVowels += 1
                return True, ''
        else:
            return False, 'Minimum 4 consonants required'

    #-----------------------------------------------------------------------  
    def Reset(self):
        self._showingLetters = []
        self._remVowels = self._allVowels[:]
        self._remConsonants = self._allConsonants[:]
        self._numConsonants = self._numVowels = 0

    #-----------------------------------------------------------------------  
    def TestWord(self, word):
        """
        Test passed word against current letters and dictionary for validity.
        """
        word = word.upper()
        remaining = self._showingLetters[:]

        #Check that word valid for current letters
        for c in word:
            if c in remaining:
                remaining.remove(c)
            else:
                return False, 'Sorry, word cannot be made from given letters.'

        res = word in self._wordList

        if res:
            return True, 'Congratulations! Word is valid.'
        else:
            return False, 'Sorry, Senor dictionary says word cannot be found.'
        

    #**********************************************************
    #--------------------- PRIVATE METHODS -------------------*
    #**********************************************************
    def _build_tiles(self):
        freq = self._letterFrequency
        vowels = []
        consonants = []

        for let in freq:
            if let in ['A', 'E', 'I', 'O', 'U']:
                vowels.append(let)
                vowels += (freq[let] - 1)*vowels[-1:]
            else:
                consonants.append(let)
                consonants += (freq[let] - 1)*consonants[-1:]

        return consonants, vowels

    #-----------------------------------------------------------------------
    def _init_dictionary(self, filename):
        wordList = []
        
        with open(filename, 'r') as f:
            for line in f:
                words = line.split(' ')
                for w in words:
                    wordList.append(w)

        return wordList
    
    #-----------------------------------------------------------------------
    def _init_letter_freq(self, filename):
        letterFrequency = {}

        with open(filename, 'r') as f:
            for line in f:
                letterFrequency[line[0].upper()] = int(line[2:].strip())

        return letterFrequency

    #-----------------------------------------------------------------------
    def _add_rand_letter(self, fromLst):
        try:
            letter = choice(fromLst)
            fromLst.remove(letter)
        except IndexError:
            print 'ERROR: _get_rand_letter attempted on empty list'
            letter = None

        if not letter:
            return False
        
        if len(self._showingLetters) < self._maxLen:
            self._showingLetters.append(letter)
        else:
            print 'ERROR: Attempted to exceed max showingLetters length'
            return False

        return True
        

    #**********************************************************
    #----------------------- PROPERTIES ----------------------*
    #**********************************************************
    @property
    def MaxLen(self):
        return self._maxLen

    @property
    def NumConsonants(self):
        return self._numConsonants

    @property
    def NumVowels(self):
        return self._numVowels

    @property
    def ShowingFull(self):
        return len(self._showingLetters) == self._maxLen

    @property
    def ShowingLetters(self):
        return self._showingLetters[:]
