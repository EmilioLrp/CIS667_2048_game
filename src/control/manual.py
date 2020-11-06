from src.control.play import PlayInterface


class Manual(PlayInterface):
    def __init__(self):
        pass

    def play(self):
        return input("Please input a move: ")
