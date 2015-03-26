from time import sleep

from adamlib.util.console_util import (
    get_response, outlined_sequence, yes_or_no_input
)
from countdown.lettersround import LettersRound
from countdown.player import Player

ESC = chr(27)         # VT100 escape character constant
CLEAR = (ESC + "[2J") # Clear screen 
HOME = (ESC + "[H")   # Move cursor to upper left corner 

class LettersRoundGame:
    def __init__(self, name='Player 1', round_time=30):
        self.player = Player(name)
        self.round = None
        self.round_time = int(round_time)
        
    def play(self):
        quit = self._write_intro()
      
        if quit:
            print('\nThanks for playing!')
            return

        while True:
            self.round = LettersRound()
            self._fill_letters()
            print(
                'You have {} seconds to determine your word.'.format(
                    self.round_time))
            do_countdown(self.round_time)
            
            self._write_score()
            response = get_response('\nEnter your word:')
            valid, msg = self.round.verify_word(response)
            
            if valid:
                self.player.score += self.round.score_word(response)

            self._write_score()
            print('\n{}'.format(msg))
            
            while True:
                again = yes_or_no_input('Play again?')
                if again:
                    break
                else:
                    print('\nThanks for playing!')
                    return
        
    def _fill_letters(self):
        self._write_score()
        self._write_showing()
        
        while not self.round.showing_full:
            response = get_response('Vowel (v) or consonant (c)?')
            
            if response in ('vowel', 'v'):
                added, msg = self.round.add_vowel()
            elif response in ('consonant', 'c'):
                added, msg = self.round.add_consonant()
            else: 
                print('\nInvalid input.')
                continue
                
            self._write_score()
            self._write_showing()
        
            if msg:
                print(msg)
            
    def _write_instructions(self):
        print('\nINSTRUCTIONS:')
        print(
            'After starting the game, choose consonant or vowel to put a', 
            'new random letter on the board.',
            'This process is repeated until there are 9 showing letters.',
            'Then, you will have',
            str(self.round_time),
            'seconds to come up with the longest single word you can,',
            'using each letter only as many times as it appears.',
            'The validity of words is determined using a Scrabble-like',
            'dictionary.\n'
        )
        
    def _write_intro(self):
        clear_screen()
        print(
            '*******************************\n' +
            '|          COUNTDOWN          |\n' +
            '|        Letters Round        |\n' +
            '*******************************\n'
        )
        
        while True:
            response = get_response(
                "Press 'p' to play, 'i' to view instructions, or 'q' to quit."
            )
            
            if response == 'i':
                self._write_instructions()
            elif response == 'p':
                return False
            elif response == 'q':
                return True

    def _write_score(self):
        mid = '  Score: {}   |'.format(self.player.score)
        top = ' '*(len(mid) - 1) + '|'
        bottom = '-'*len(mid)
        
        clear_screen()
        print('{}\n{}\n{}'.format(top, mid, bottom))
        
    def _write_showing(self):
        showing = self.round.showing[:]
        showing += [' ']*(self.round.max_letters - len(showing))

        print('\n' + outlined_sequence(showing) + '\n')

def clear_screen():
    print(CLEAR)
    print(HOME)

def do_countdown(secs, post='seconds remaining...'):
    for i in range(secs, 0, -1):
        print('\r{:02d} {}   '.format(i, post), end='')
        sleep(1)
    
    print('\r{:02d} {}   \n'.format(0, post), end='')

if __name__ == '__main__':
    game = LettersRoundGame(round_time=5)
    game.play()
