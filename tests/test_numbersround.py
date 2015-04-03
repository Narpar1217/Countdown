import pytest

from countdown.numbersround import NumbersRound, NumbersRoundError

@pytest.fixture
def dummy_nr():
    nr = NumbersRound()
    nr._goal = 506
    nr._showing = [100, 2, 5, 1, 2, 8]
    
    return nr

def test_check_answer(dummy_nr):
    nr = dummy_nr
    
    # 506 (exact)
    score, msg = nr.check_answer('100*5 + 8 - 2')
    assert score == 10
    
    # 507 (off by 1)
    score, msg = nr.check_answer('100*5 + 8 - 1')
    assert score == 7
    
    # 502 (off by 5)
    score, msg = nr.check_answer('100*5 + 1')
    assert score == 7
    
    # 496 (off by 10)
    score, msg = nr.check_answer('100*5 - (2*2)')
    assert score == 5
    
    # Off by a lot
    # Trailing newline
    # All numbers and operations/valid characters (except all digits) used
    score, msg = nr.check_answer('100 + 2 - 5*1 + (8 / 2)\n')
    assert score == 0

def test_check_answer_num_not_in_showing(dummy_nr):
    nr = dummy_nr
    
    score, msg = nr.check_answer('506')
    assert score is None
    assert msg
    
    score, msg = nr.check_answer('100*5 + 6')
    assert score is None
    assert msg

def test_check_answer_invalid_chars(dummy_nr):
    nr = dummy_nr
    
    # Try something dangerous
    score, msg = nr.check_answer('sys.exit(1)')
    assert score is None
    assert msg
    
    score, msg = nr.check_answer("print(os.listdir('.'))")
    assert score is None
    assert msg
    
    # Exponentiation
    score, msg = nr.check_answer('5**2 + 8')
    assert score is None
    assert msg

def test_initial_state():
    nr = NumbersRound()
    
    assert nr.showing is None
    assert nr.goal in range(100, 1000)

def test_normal_play():
    nr = NumbersRound()
    
    msg = nr.set_showing(3)
    assert not msg
    
    answer = '+'.join(str(n) for n in nr.showing)
    score, msg = nr.check_answer(answer)
    
    assert score in (0, 5, 7, 10)
    assert isinstance(msg, str)

def test_set_readonly_attributes():
    nr = NumbersRound()
    
    with pytest.raises(AttributeError):
        nr.goal = 120
    
    with pytest.raises(AttributeError):
        nr.showing = [1, 2, 3]

def test_set_showing():
    def do_one_test(n):
        nr = NumbersRound()
        nr.set_showing(n)
    
        assert nr._showing is not nr.showing
        assert nr._showing == nr.showing
        assert len(nr.showing) == nr._MAX_TILES
    
        for sn in nr.showing:
            assert type(sn) == int
            assert 1 <= sn <= 100
            
    for i in range(5):
        do_one_test(i)

    do_one_test('0')
    do_one_test(4.0)
    do_one_test('3\n')

def test_set_showing_multiple_calls():
    nr = NumbersRound()
    nr.set_showing(4)
    
    with pytest.raises(NumbersRoundError):
        nr.set_showing(3)
    
def test_set_showing_bad_values():
    def assert_error(num_large):
        nr = NumbersRound()
        msg = nr.set_showing(num_large)
        assert isinstance(msg, str)
        assert msg
        
    assert_error(5)
    assert_error('-1')
    assert_error([4])
    assert_error('one')
