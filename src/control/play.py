from abc import ABCMeta, abstractmethod
from src.game.game import Game

"""
Interface for play, all other control should implement this interface 
"""


class PlayInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def play(self, game: Game): raise NotImplementedError

    @abstractmethod
    def play_auto(self, game:Game): raise NotImplementedError
