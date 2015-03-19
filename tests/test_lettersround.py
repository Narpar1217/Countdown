import pytest

from countdown.lettersround import LettersRound, LettersRoundError

@pytest.fixture
def consonants():
    return [c.upper() for c in 'bcdfghjklmnpqrstvwxyz']

@pytest.fixture
def vowels():
    return [v.upper() for v in 'aeiou']

def test_basic(consonants, vowels):
    lr = LettersRound()

    for i in range(lr.max_consonants):
        assert lr.add_consonant()[0] == True
        assert lr.showing[-1] in consonants
        assert not lr.showing_full

    for i in range(lr.min_vowels):
        assert lr.add_vowel()[0] == True
        assert lr.showing[-1] in vowels

    assert lr.showing_full

def test_too_many_vowels(vowels):
    lr = LettersRound()
    
    for i in range(lr.max_vowels):
        assert lr.add_vowel()[0] == True
        assert lr.showing[-1] in vowels

    assert lr.num_vowels == lr.max_vowels

    assert lr.add_vowel()[0] == False

def test_too_many_consonants(consonants):
    lr = LettersRound()

    for i in range(lr.max_consonants):
        assert lr.add_consonant()[0] == True
        assert lr.showing[-1] in consonants

    assert lr.num_consonants == lr.max_consonants

    assert lr.add_consonant()[0] == False

def test_too_many_letters(consonants, vowels):
    lr = LettersRound()
    
    # Fill showing
    for i in range(lr.max_consonants):
        lr.add_consonant()
        assert lr.showing[-1] in consonants
        assert not lr.showing_full

    for i in range(lr.min_vowels):
        lr.add_vowel()
        assert lr.showing[-1] in vowels

    assert lr.showing_full

    # Try to add another letter
    with pytest.raises(LettersRoundError):
        lr.add_vowel()
