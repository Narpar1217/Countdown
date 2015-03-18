from os import stat
from os.path import isfile

from countdown.game.resmaps import WORDLIST_PATH

def test_wordlist_exists():
    # Assert file exists
    assert isfile(WORDLIST_PATH)

    # Assert file is not empty
    statinfo = stat(WORDLIST_PATH)
    assert statinfo.st_size > 0

def test_wordlist_format():
    """Verify words in wordlist separated only by space(s)"""
    with open(WORDLIST_PATH) as f:
        i = None
        for i, line in enumerate(f.readlines()):
            for word in line.split(' '):
                # An empty word means multiple spaces separate two words
                assert word

        # Verify there are no newlines in the file
        assert i == 0
        
