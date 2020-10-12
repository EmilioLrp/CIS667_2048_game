import numpy as np
# from actions import Action
from getkey import getkey
import random


class Board:
    def __init__(self):
        self._board_size = 4
        self._game_board = np.zeros((self._board_size, self._board_size), dtype=int)
        self._init_game()

    def _init_game(self):
        # action = Action()
        # self.actions = action.get_action()
        # generate 2 tiles with value 2 at random position
        self._generate_rand_tile()
        self._generate_rand_tile()

    def _generate_rand_tile(self):
        empty = np.argwhere(self._game_board == 0)
        tile = random.sample(list(empty), 1)
        self._game_board[tile[0][0]][tile[0][1]] = 2

    def valid_action(self, action):
        pass

    def display(self):
        print(self._game_board)

    def update_state(self, move):
        if self.valid_action(action=move):
            pass

    def game_over(self):
        return False

    def play_move(self):
        # @TODO: override with tree search and machine learning algs
        while True:
            key = getkey()
            if key in self.actions.values():
                break
        return key


if __name__ == '__main__':
    board = Board()
    move_count = 0
    board.display()
    while True:
        if board.game_over():
            print("")
            break
        action = input("Please input a move: ")
        if not board.valid_action(action=action):
            continue
        # @TODO update game board
    # while True:
    #     move = board.play_move()
    #     move_count += 1
    #     board.update_state(move=move)
    #     board.display()
    #     if board.game_over():
    #         break
    # print("Total move used: %d" % move_count)
