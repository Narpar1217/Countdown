from countdown.player import Player

def test_name():
    p = Player('Mickey')
    assert p.name == 'Mickey'

    p = Player('mickey mouse')
    assert p.name == 'Mickey Mouse'

    p.name = 'donald'
    assert p.name == 'Donald'

    p.name = 'donald Duck'
    assert p.name == 'Donald Duck'

    p.name = 'player 1'
    assert p.name == 'Player 1'

    p.name = '127.0.0.1'
    assert p.name == '127.0.0.1'
    
def test_score():
    p = Player('name')
    assert p.score == 0

    p.score = 4
    assert p.score == 4

    p.score += 2
    assert p.score == 6

    p.score = '3'
    assert p.score == 3

    p.score += 5.0
    assert p.score == 8

    p.score -= 10
    assert p.score == -2

    p.score *= -1
    assert p.score == 2
