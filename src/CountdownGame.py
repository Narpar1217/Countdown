"""
Copyright (C) 2013 Adam Beagle - All Rights Reserved
You may use, distribute, and modify this code under
the terms of the GNU General Public License,
viewable at http://opensource.org/licenses/GPL-3.0

This copyright notice must be retained with any use
of source code from this file.
"""

from LettersGame import LettersGame
from NumbersGame import NumbersGame
from CountdownPlayer import CountdownPlayer

class CountdownGame(object):
    """"""

    #**********************************************************
    #---------------------- CONSTRUCTOR ----------------------*
    #**********************************************************
    def __init__(self, players=[], roundTime=30):
        """
        Constructor. players should be list of tuples of form (name, 'client'|'server'|'')
        """
        self._lg = LettersGame()
        self._ng = NumbersGame()

        self.RoundTime = roundTime

        self._players = []

        if players:
            for name, pType in players:
                self.AddPlayer(name, pType)


    #**********************************************************
    #--------------------- PUBLIC METHODS --------------------*
    #**********************************************************
    def AddPlayer(self, name, pType=''):
        """Accepted values for pType are ('client', 'server')"""

        if pType.lower() in ('client', 'server'):
            self._players.append(CountdownPlayer(name, pType.lower()))
        elif pType:
            raise ValueError("Invalid pType supplied to AddPlayer. Use 'client' or 'server'") 
        else:
            self._players.append(CountdownPlayer(name))


    #**********************************************************
    #----------------------- PROPERTIES ----------------------*
    #**********************************************************
    @property
    def LettersGame(self):
        return self._lg

    #---------------------------------------------------------
    @property
    def NumbersGame(self):
        return self._ng

    #---------------------------------------------------------
    @property
    def NumPlayers(self):
        return len(self._players)

    #---------------------------------------------------------
    @property
    def Players(self):
        return self._players

    #---------------------------------------------------------
    @property
    def RoundTime(self):
        return self._roundTime

    @RoundTime.setter
    def RoundTime(self, value):
        if not value or int(value) < 0:
            self._roundTime = 30
        else:
            self._roundTime = int(value)

    #---------------------------------------------------------
    @property
    def ServerPlayer(self):
        return [x for x in self._players if x.PType == 'server'][0]



#########################################################################
if __name__ == '__main__':
    g = CountdownGame([('Adam', 'server'), ('Claire', 'client')])
