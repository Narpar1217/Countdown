"""
NumbersGame.py

Based on one of the games played in the game show Countdown. 

General Description:
Two piles of numbers, for large and small, exist (defined in more detail below).
A player chooses how many numbers he/she wants out of each of these piles, for a total of 6 numbers.
Those numbers of values are then randomly chosen from the piles, and become the set of manipulatable
values for the round.
Finally, a 3-digit target integer is randomly generated.
The players must use basic arithmetic on the set of numbers, using any subset of numbers in the set,
to get as close to possible to the target.
Scores are then given based on how close each player gets. 
Solutions within 10 of the target score points, increasing in value the closer the solution (see GetScore).
"""

from random import randint, choice
import sys
import re

###############################################################################
class NumbersGame(object):
    """Defines a Countdown-style Numbers Game.
    Includes capability to randomly generate target and 
    manipulatable numbers, and check player solutions
    against those values."""

    #**********************************************************
    #---------------------- CONSTRUCTOR ----------------------*
    #**********************************************************
    def __init__(self):
        self._largeNums = []
        self._smallNums = []
        self._size = 6
        self._target = 0
        self._rndNums = []
        
        self._init_numbers()

    #**********************************************************
    #--------------------- PUBLIC METHODS --------------------*
    #**********************************************************
    def NewRound(self, numLarge):
        """
        Sets up new round. Sets and returns list of round numbers, and target.
        numLarge is the number of selections from the 'large numbers' pile the
        player requested. 
        """
        self._init_numbers()
    
        self._set_lg_sm_numbers(numLarge)
        self._set_target_random()

        return self._rndNums, self._target

    #-------------------------------------------------------------------------
    def CheckSolution(self, sltn):
        """
        Checks passed solution string for validity and distance from target.
        If solution was able to be parsed, the return values are True and the distance from target.
        Otherwise, False and an error description string are returned.

        With the exception of converting 'x/X' to '*', strings are treated as
        python lines, i.e. eval(sltn) is used, so order of operations is important!
        """
        valid = False

        sltn, msg = self._cleanup_sltn_str(sltn)

        if msg:
            return False, msg

        try:
            result = eval(sltn)
        except SyntaxError as e:
            diff = 'Error of {0} occured when parsing solution.\nLikely causes: Asymmetric parentheses, invalid operators'.format(type(e))
        except NameError as e:
            diff = 'Error of {0} occured when parsing solution.\nLikely cause: Character(s) aside from digits, parens, or math operators included.'.format(type(e))
        except:
            print >>sys.stderr, "Unexpected error:", sys.exc_info()[0]
            raise
        else:
            inRnd, msg = self._check_soltn_nums_valid(sltn)

            if inRnd:
                valid = True
                diff = self._target - int(result)
            else:
                diff = msg
            
        return valid, diff

    #-------------------------------------------------------------------------
    def GetScore(self, diff):
        """
        Returns score based on difference from target.
        Score brackets are as defined on the Countdown Wkipedia page.
        """
        diff = abs(int(diff))
        
        if diff == 0:
            score = 10
        elif diff <= 5:
            score = 7
        elif diff <= 10:
            score = 5
        else:
            score = 0

        return score

    #**********************************************************
    #--------------------- PRIVATE METHODS -------------------*
    #**********************************************************
    def _check_soltn_nums_valid(self, sltn):
        """
        Checks that any numbers in sltn are in round numbers,
        including ensuring numbers are only used as many times
        as appropriate.

        Returns boolean representing representing validity, and error message
        if needed.
        """
        nums = [int(x) for x in re.findall('\d+\.?\d*', sltn)]
        rnd = self.Numbers[:]

        for n in nums:
            if not n in rnd:
                return False, "{0} not found in remaining numbers: {1}".format(n, rnd)
            else:
                rnd.remove(n)

        return True, ''
                
    #-------------------------------------------------------------------------
    def _cleanup_sltn_str(self, sltn):
        try:
            sltn = str(sltn).lower()
        except:
            return sltn, 'ERROR: Problem with passed solution. Cannot be converted to string for evaluation.\n' + sys.exc_info()[0]
        else:
            sltn = sltn.replace('x', '*')
            sltn = sltn.replace('\\', '/')

        return sltn, ''

    #-------------------------------------------------------------------------
    def _init_numbers(self):
        """
        (Re)Sets largeNums and smallNums to their initial values as defined on the Countdown Wikipedia page.
        """
        self._largeNums = [25, 50, 75, 100]
        smallNums = []

        for i in xrange(1, 10):
            smallNums += 2*[i]

        self._smallNums = smallNums
    #-------------------------------------------------------------------------
    def _set_lg_sm_numbers(self, numLarge):
        """
        Note: While this function fixes cases where numLarge is not between 0 and 4,
        it gives no warning that it is doing so. Checking to ensure a valid value should be
        done elsewhere.
        """
        self._rndNums = []
        
        try:
            numLarge = int(numLarge)
        except ValueError:
            print >>sys.stderr, 'ERROR: Passed value for numLarge must be numeric. Defaulting to 0.'
            numLarge = 0
        
        if numLarge > 4:
            numLarge = 4
        elif numLarge < 0:
            numLarge = 0
            
        for i in xrange(numLarge):
            lg = choice(self._largeNums)
            self._largeNums.remove(lg)
            self._rndNums.append(lg)
            

        for i in xrange(self._size - numLarge):
            sm = choice(self._smallNums)
            self._smallNums.remove(sm)
            self._rndNums.append(sm)

    #-------------------------------------------------------------------------
    def _set_target_random(self):
        self._target = randint(100, 999)


    #**********************************************************
    #----------------------- PROPERTIES ----------------------*
    #**********************************************************
    @property
    def Numbers(self):
        return self._rndNums

    @property
    def Target(self):
        return self._target



#################################################################################################
if __name__ == '__main__':
    #test data, normally this class would be instantiated and used elsewhere.
    g = NumbersGame()
    g.NewRound(2)
    print g.Numbers, g.Target
