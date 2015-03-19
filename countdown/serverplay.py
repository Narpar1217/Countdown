"""
serverplay.py
Author: Adam Beagle

PURPOSE:
  Provides a text-only version of Countdown playable over a server.
  Currently only letters rounds are implemented.
  
USAGE:
  Call play_letters_round, providing a readable stream and writable stream.
"""
from adamlib.util.console_util import tabular_sequence
from adamlib.util.serversocket_util import get_response, write_countdown
from countdown.lettersround import LettersRound
from countdown.player import Player

ESC = chr(27)                  # VT100 escape character constant
CLEAR = (ESC + "[2J").encode() # Clear screen 
HOME = (ESC + "[H").encode()   # Move cursor to upper left corner 

def clear(wfile):
    """
    Send VT100 clear screen sequence to writable stream `wfile`, and return
    cursor to upper left with VT100 home sequence.
    
    Return:
      None
    """
    wfile.write(CLEAR)
    wfile.write(HOME)
    
def clear_and_write_score(wfile, score):
    """
    Clear screen with clear() and write score at upper left with write_score().
    
    Return:
      None
    """
    clear(wfile)
    write_score(wfile, score)

def fill_letters(rfile, wfile, round, player):
    """
    Repeatedly ask user for vowel or consonant until round.max_letters is
    reached. On each iteration, the screen is cleared and redrawn to reflect
    the updated game board.
    
    Input:
      `rfile` - readable stream
      `wfile` - writable stream
      `round` - countdown LettersRound object
      `player` - countdown Player object
    
    Return:
      None
    """
    clear_and_write_score(wfile, player.score)
    wfile.write(b'\n\n\n\n')
    
    while not round.showing_full:
        response = get_response(rfile, wfile, 'Vowel (v) or consonant (c)?')
        
        if response in ('vowel', 'v'):
            added, msg = round.add_vowel()
        elif response in ('consonant', 'c'):
            added, msg = round.add_consonant()
        else: 
            wfile.write(b'Invalid input.\n')
            continue

        clear_and_write_score(wfile, player.score)
        write_showing(wfile, round.showing)
        
        if msg:
            wfile.write(msg.encode() + b'\n')

def play_letters_round(rfile, wfile, round_time=30):
    """
    Input:
      `rfile` - readable file-like object
      `round_time` - integer (in seconds)
      `wfile` - writable file-like object
      
    Return:
      None
    """
    player = Player('Player 1')
    
    quit = write_intro(rfile, wfile, round_time)
    if quit:
        return
    
    while True:
        round = LettersRound()
        fill_letters(rfile, wfile, round, player)
        
        wfile.write(
            ('You have {} seconds '.format(round_time) + 
            'to determine your word. Go!\n').encode()
        )
        write_countdown(wfile, round_time)

        clear_and_write_score(wfile, player.score)
        response = get_response(rfile, wfile, '\r\nEnter your word:')
        valid, msg = round.verify_word(response)
        
        if valid:
            player.score += round.score_word(response)
            
        clear_and_write_score(wfile, player.score)
        wfile.write(b'\n' + msg.encode() + b'\n')
        
        while True:
            response = get_response(rfile, wfile, 'Play again? (y or n)')
            if response in ('y', 'yes'):
                break
            elif response in ('n', 'no'):
                return

def write_instructions(wfile, round_time):
    """
    Return:
      None
    """
    wfile.write(b'\n\nDESCRIPTION:\n')
    wfile.write(b''.join([
        b'This game is a stripped-down, web-only version of my game ',
        b'"Countdown." It was made as a hobbyist project. ',
        b'For more information, see http://adambeagle.com/projects'
    ]))
    wfile.write(b'\n\nINSTRUCTIONS:\n')
    wfile.write(b''.join([
        b'Choose consonant or vowel until there are 9 showing letters. ',
        b'Then, you will have ',
        str(round_time).encode(),
        b' seconds to come up with the longest single ',
        b'word you can, using each letter only as many times as it appears.',
        b'\n\n',
    ]))

def write_intro(rfile, wfile, round_time):
    """
    Write title and ask give user options to play, print instructions, 
    or quit. 
    
    Return:
      True if user desires to quit, otherwise False.
    """
    clear(wfile)
    wfile.write(b'*******************************\n')
    wfile.write(b'|          COUNTDOWN          |\n')
    wfile.write(b'|        Letters Round        |\n')
    wfile.write(b'*******************************\n\n')

    # Loop until valid response
    while True:
        response = get_response(
            rfile, 
            wfile, 
            "Press 'p' to play, 'i' to view instructions, or 'q' to quit."
        )

        if response == 'i':
            write_instructions(wfile, round_time)
        elif response == 'p':
            return False
        elif response == 'q':
            return True
            
def write_score(wfile, score=0):
    """
    Write to stream `wfile` a box containing `score.`
    Score is always padded on both sides with two spaces.
    
    Return:
      None
    
    Example:
                |
      Score: 0  |
    -------------
    """
    mid = '  Score: {}   |'.format(score)
    top = ' '*(len(mid) - 1) + '|'
    bottom = '-'*len(mid)
    
    wfile.write('{}\n{}\n{}\n'.format(top, mid, bottom).encode())

def write_showing(wfile, showing):
    """
    Write prettified version of iterable `showing` to stream `wfile.`
    See tabular_sequence() for formatting.
    If showing is empty, nothing is written.
    
    Return:
      None
    """
    lines = tabular_sequence(showing)
    
    if lines:
        wfile.write(b'\n' + lines.encode() + b'\n\n')