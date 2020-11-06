from abc import ABCMeta, abstractmethod

"""
Interface for play, all other control should implement this interface 
"""


class PlayInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def play(self): raise NotImplementedError
