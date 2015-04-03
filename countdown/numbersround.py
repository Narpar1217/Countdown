from random import randint, shuffle
from re import finditer, match, search

class NumbersRoundError(Exception):
    pass

class NumbersRound:
    """
    USAGE:
      1. For every round, instantiate a new object of this class.
      
      2. To set the random list of showing tiles for the round, call 
         set_showing(), passing the number of large numbers to use (which should
         be a response from the user).
         
      3. Use check_answer() to verify that a user's answer is valid, and
         if so score it.
    
    ATTRIBUTES:
      goal (read-only)
      showing (read-only)
    
    METHODS:
      check_answer(answer)
      set_showing(num_large)
    """
    _MAX_TILES = 6
    
    def __init__(self):
        self._showing = None
        self._goal = randint(100, 1000)
        
        self._large_number_bag = [25, 50, 75, 100]
        self._small_number_bag = list(range(1, 11))*2
        shuffle(self._large_number_bag)
        shuffle(self._small_number_bag)
        
    def check_answer(self, answer):
        """
        Return (score, msg) based on `answer`.
        
        If the answer uses invalid characters or could not be parsed, 
        score is None and msg contains a description of the problem.
        """
        answer = answer.strip()
        msg = self._verify_answer_string(answer)

        try:
            if not msg:
                # Global/local state not passed
                answer_n = eval(answer, {}, {})
        except SyntaxError as e:
            msg = (
                'There was a syntax error while parsing your answer. ' +
                'Make sure parentheses are matched, and that you are only ' +
                'using +, -, *, and / as operations.'
            )
        except Exception as e:
            msg = (
                'An error occurred while evaluating the answer:\n{}'.format(e)
            )

        if msg:
            return None, msg
        else:
            return self._score(answer_n), 'Answer is valid! '
        
    def set_showing(self, num_large):
        """
        Populate the `showing` attribute with random numbers.
        The number of large numbers is determined by `num_large`.
        
        Return an empty string if successful, or an error message with a
        description of the problem.
        
        Raises NumbersRoundError if called more than once in the same round.
        """
        max_large = len(self._large_number_bag)
        numbers = []
        return_msg = ''
        msg_on_invalid_input = (
            'Number of large numbers must be number between ' +
            '0 and {}'.format(max_large)
        )
        
        if self._showing is not None:
            raise NumbersRoundError(
                "Showing numbers already set for this round. " +
                "Access them with the 'showing' attribute."
            )
        
        # Attempt cast of num_large to int, verify num_large in valid range.
        try:
            num_large = int(num_large)
            
            if not 0 <= num_large <= max_large:
                return_msg = msg_on_invalid_input
                
        except (ValueError, TypeError):
            return_msg = msg_on_invalid_input
        
        # If num_large valid, put values in self._showing
        if not return_msg:
            numbers += [self._next_large_number() for i in range(num_large)]
            numbers += [self._next_small_number() 
                for i in range(self._MAX_TILES - num_large)
            ]
            shuffle(numbers)
            
            self._showing = numbers
            
        return return_msg

    def _next_small_number(self):
        return self._small_number_bag.pop()
        
    def _next_large_number(self):
        return self._large_number_bag.pop()
        
    def _score(self, n):
        diff = abs(self.goal - n)
        
        if diff == 0:
            return 10
            
        elif 1 <= diff <= 5:
            return 7
            
        elif 6 <= diff <= 10:
            return 5
            
        else:
            return 0
            
    def _verify_answer_string(self, answer):
        msg = ''
        
        if not match('^[0-9/+\-*() ]+$', answer):
            msg = (
                'Invalid answer. Answers may be comprised only of digits, ' +
                'spaces, parentheses, and arithmetic symbols (+, -, *, /).'
            )
            
        elif search('\*\*|//', answer):
            msg = (
                'Invalid answer. Exponentiation (**) and floor division (//)' + 
                ' are not allowed. Valid operations are +, -, *, and /. '
            )
        
        else:
            # Verify all numbers in answer appear in showing
            showing = self.showing # Note this makes a copy of self._showing
            
            for match_ in finditer('[\d]+', answer):
                n = int(match_.group(0))
                if n not in self._showing:
                    msg = (
                        'Invalid answer. A number not from the showing' + 
                        'tiles ({}) was used.'.format(n)
                    )
                    break
                    
                showing.remove(n)
                
        return msg

    @property
    def goal(self):
        return self._goal
        
    @property
    def showing(self):
        return self._showing[:] if self._showing is not None else None
    
