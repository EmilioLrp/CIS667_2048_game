from src.control.play import PlayInterface
from src.game.game import Game


class Manual(PlayInterface):
    def __init__(self):
        pass

    def play(self, game: Game) -> (str, int):
        return input("Please input a move: "), 1

    def play_auto(self, game:Game):
        pass