"""
Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""

from sys import stderr

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
                print >>stderr, 'ERROR: Attempted to set score with invalid data. Defaulting to 0. Bad value: ', str(value)
                self._score = 0
