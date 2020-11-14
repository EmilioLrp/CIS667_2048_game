from src.control.play import PlayInterface
from src.game.game import Game
import random


class URand(PlayInterface):
    def __init__(self):
        pass

    def play(self, game: Game):
        input("Press Enter to continue:")
        return self.play_game(game=game)

    def play_game(self, game: Game):
        return random.choice(game.valid_actions()), 1
