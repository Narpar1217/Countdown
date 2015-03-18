from os import stat
from os.path import isfile

import pytest

from countdown.game.lettersround import InitError, WordList
from countdown.game.resmaps import WORDLIST_PATH

def test_wordlist_file_exists():
    assert isfile(WORDLIST_PATH)

    # Assert file is not empty
    statinfo = stat(WORDLIST_PATH)
    assert statinfo.st_size > 0

def test_wordlist_file_format():
    """Verify words in wordlist separated only by space(s)"""
    with open(WORDLIST_PATH) as f:
        i = None
        for i, line in enumerate(f.readlines()):
            for word in line.split(' '):
                # An empty word means multiple spaces separate two words
                assert word

        # Verify there are no newlines in the file
        assert i == 0
        
def test_wordlist():
    def do_tests(wlist):
        wlist.init(WORDLIST_PATH)
        assert wlist.wordlist is not None
        assert wlist.search('some')
        assert wlist.search('word')
        assert not wlist.search('some word')
        
    wlist = WordList()
    do_tests(wlist)

    # Use of an instance or the class itself should have identical functionality
    wlist = WordList
    do_tests(wlist)

    # Verify that initialization remains despite new instance.
    wlist = WordList()
    assert wlist.search('some')
