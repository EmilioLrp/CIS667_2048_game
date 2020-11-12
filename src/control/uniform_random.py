from src.control.play import PlayInterface
from src.game.game import Game
import random


class URand(PlayInterface):
    def __init__(self):
        pass

    def play(self, game: Game):
        return random.choice(game.valid_actions())
