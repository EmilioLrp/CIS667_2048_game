import numpy as np
import random


class Board:
    def __init__(self):
        self._board_size = 4
        self._game_board = np.zeros((self._board_size, self._board_size), dtype=int)
        self._init_game()

    def _init_game(self):
        # generate 2 tiles with value 2 at random position
        self._generate_rand_tile()
        self._generate_rand_tile()

    def _generate_rand_tile(self):
        empty = np.argwhere(self._game_board == 0)
        tile = random.sample(list(empty), 1)
        self._game_board[tile[0][0]][tile[0][1]] = 2

    def merge_tile(self, line):
        pass
