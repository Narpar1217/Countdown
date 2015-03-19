"""
player.py
Author: Adam Beagle

PURPOSE:
  Contains Player class, which defines a Countdown player.
"""
class ScoreError(Exception):
    pass

class Player:
    """ """
    def __init__(self, name):
        self.name = name
        self._score = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value).title()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        try:
            self._score = int(value)
        except (TypeError, ValueError):
            raise ScoreError(
                "score expects object castable to int. Got {}".format(value)
            )

