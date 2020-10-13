from actions import Action
from board import Board


class Game:
    def __init__(self):
        self._game_board = Board()

    def display(self):
        print(self._game_board)

    def update_state(self, action):
        if action == Action.left:
            line = []
            self._game_board.merge_tile(line=line)
            pass
        elif action == Action.right:
            pass

    def valid_action(self, action):
        pass

    def game_over(self):

        return False


if __name__ == '__main__':
    game = Game()
    move_count = 0
    game.display()
    while True:
        if game.game_over():
            print("")
            break
        action = input("Please input a move: ")
        if not game.valid_action(action=action):
            continue
            # @TODO update game board
