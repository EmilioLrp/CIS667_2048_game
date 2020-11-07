import numpy as np
import random


class Board:
    def __init__(self):
        self._board_size = 4
        self._game_board = np.zeros((self._board_size, self._board_size), dtype=int)
        self._total_score = 0
        self._init_game()
        self._new_pos = None  # the position of the new random generated tile

    # def test_board(self, board):
    #     self._game_board = np.copy(board)

    def get_board(self) -> np.ndarray:
        return self._game_board

    def get_score(self) -> int:
        return self._total_score

    def get_size(self) -> int:
        return self._board_size

    def get_new_pos(self) -> (int, int):
        return self._new_pos

    def _init_game(self):
        # generate 2 tiles with value 2 at random position
        self._generate_rand_tile()
        self._generate_rand_tile()

    def _generate_rand_tile(self):
        empty = np.argwhere(self._game_board == 0)
        tile = random.sample(list(empty), 1)
        # print("random number generated at %s" % str(tile[0]))
        self._new_pos = (tile[0][0], tile[0][1])
        self._game_board[tile[0][0], tile[0][1]] = 2

    def merge_tile(self, lines: list, merge_to_left: bool = True):
        """
        This function process the lines that extracted according to the direction of user's movement
        :param lines: list of line that extracted from the game board according to the user's movement
        each element of line: pair of x, y coordinate of the tile
        :param merge_to_left: controls the direction of merging
        :return:
        """

        for line in lines:
            if not merge_to_left:
                # flip the line so that it performs the same as merging to the left of the array
                line = np.flip(line, 0)
            # move all elements in the line to the far left first
            self._shift_line(line=line)
            for i in range(len(line) - 1):
                if self._get_tile(line, i) == 0:
                    break
                # a sliding window is applied
                j = i + 1
                start_tile = self._get_tile(line, i)
                end_tile = self._get_tile(line, j)
                if start_tile == end_tile:
                    tile_sum = start_tile + end_tile
                    self._game_board[line[i][0], line[i][1]] = tile_sum
                    self._total_score += tile_sum
                    self._merge_line(line, start_at=j)
        self._generate_rand_tile()

    def _shift_line(self, line: list):
        board_line = []
        for i in line:
            board_line.append(self._game_board[i[0], i[1]])
        board_line = [nonZero for nonZero in board_line if nonZero != 0] + [Zero for Zero in board_line if Zero == 0]
        for i in range(len(line)):
            index = line[i]
            self._game_board[index[0], index[1]] = board_line[i]

    def _merge_line(self, line: list, start_at: int):
        for i in range(start_at, len(line) - 1):
            j = i + 1
            # move each tile to the left of the line by 1
            self._game_board[line[i][0], line[i][1]] = self._game_board[line[j][0], line[j][1]]
        self._game_board[line[len(line) - 1][0], line[len(line) - 1][1]] = 0

    def _get_tile(self, line: list, line_index: int):
        x = line[line_index][0]
        y = line[line_index][1]
        return self._game_board[x, y]

    def movable(self, lines: list, to_left: bool) -> bool:
        for line in lines:
            if not to_left:
                line = np.flip(line, 0)
            board_line = []
            zero_index = []
            for i in range(len(line)):
                tile = self._get_tile(line, i)
                if tile == 0:
                    zero_index.append(i)
                board_line.append(tile)
            board_line = np.array(board_line)
            if len(zero_index) != 0 and np.count_nonzero(board_line[zero_index[0]:]) != 0:
                # count from the first 0, if it exists
                # if the rest of the list contains at least 1 non zero, the line is movable
                return True
            for i in range(len(board_line[board_line != 0]) - 1):
                j = i + 1
                if self._get_tile(line, i) == self._get_tile(line, j):
                    # a sliding window
                    # if 2 contingent tiles contains same value, then this line is movable
                    return True
        return False
