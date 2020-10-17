import numpy as np
import random


class Board:
    def __init__(self):
        self._board_size = 4
        self._game_board = np.zeros((self._board_size, self._board_size), dtype=int)
        self._init_game()

    def get_board(self):
        return self._game_board

    def get_size(self):
        return self._board_size

    def _init_game(self):
        # generate 2 tiles with value 2 at random position
        self._generate_rand_tile()
        self._generate_rand_tile()

    def _generate_rand_tile(self):
        empty = np.argwhere(self._game_board == 0)
        tile = random.sample(list(empty), 1)
        self._game_board[tile[0][0]][tile[0][1]] = 2

    def merge_tile(self, lines, merge_to_left=True):
        """
        This function process the lines that extracted according to the direction of user's movement
        :param lines: list of line that extracted from the game board according to the user's movement
        each element of line: pair of x, y coordinate of the tile
        :param merge_to_left: controls the direction of merging
        :return:
        """
        for line in lines:
            if not merge_to_left:
                line = np.flip(line, 0)
            for i in range(len(line) - 1):
                j = i + 1
                start_tile = self._get_tile(line, i)
                end_tile = self._get_tile(line, j)
                if start_tile == end_tile:
                    self._game_board[line[i][0], line[i][1]] = start_tile + end_tile
                    self._merge_line(line, index=j)
        self._generate_rand_tile()

    def _merge_line(self, line, index):
        for i in range(index, len(line-1)):
            j = i + 1
            # move each tile to the left of the line by 1
            self._game_board[line[i][0], line[i][1]] = self._game_board[line[j][0], line[j][1]]
        self._game_board[line[len(line)-1][0], line[len(line)-1][1]] = 0

    def _get_tile(self, line, line_index):
        x = line[line_index][0]
        y = line[line_index][1]
        return self._game_board[x,y]
