"""
Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""

from Player import Player

################################################################################
class CountdownPlayer(Player):
    """"""
    # ~~~ CONSTRUCTOR ~~~
    def __init__(self, name='', pType='', score=0):
        super(CountdownPlayer, self).__init__(name, score)

        self._pType = pType
        self._last = False


    # ~~~ PROPERTIES ~~~
    @property
    def PType(self):
        return self._pType

    @property
    def LastToPick(self):
        return self._last

    @LastToPick.setter
    def LastToPick(self, value):
        self._last = bool(value)
    
