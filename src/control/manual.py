from src.control.play import PlayInterface
from src.game.game import Game


class Manual(PlayInterface):
    def __init__(self):
        pass

    def play(self, game: Game) -> str:
        return input("Please input a move: ")
