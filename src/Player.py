################################################################################
class Player(object):
    """Defines a generic player for a game. Includes attributes for name and score."""

    #**********************************************************
    #---------------------- CONSTRUCTOR ----------------------*
    #**********************************************************
    def __init__(self, name='', score=0):
        self.Name = name
        self.Score = score

    #**********************************************************
    #----------------------- PROPERTIES ----------------------*
    #**********************************************************
    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, value):
        self._name = str(value)

    #---------------------------------------------------------
    @property
    def Score(self):
        return self._score

    @Score.setter
    def Score(self, value):
        if isinstance(value, (int, float, long)):
            self._score = value
        else:
            try:
                n = float(value)
                if n % 1 == 0.0:
                    n = int(n)

                self._score = n
            except (ValueError, TypeError):
                print 'ERROR: Attempted to set score with invalid data. Defaulting to 0. Bad value: ', str(value)
                self._score = 0
