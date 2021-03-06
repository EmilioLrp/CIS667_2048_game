import numpy as np
import math
from src.game.board import Board

from src.game.actions import Action


class Game:
    def __init__(self):
        self._game_board = None
        self._board_indexes = None
        self._goal = None
        self._move_count = 0
        self._weighted_score = 0
        self.init_board(size=4, goal=2048)

    def init_board(self, size, goal):
        self._game_board = Board(size=size)
        self._board_indexes = Game._game_board_indexes(self._game_board.get_size())
        self._goal = goal

    @classmethod
    def _game_board_indexes(cls, size) -> np.ndarray:
        board_index = np.ndarray(shape=(size, size), dtype=object)
        for r in range(board_index.shape[0]):
            for c in range(board_index.shape[1]):
                board_index[r, c] = (r, c)
        return board_index

    def get_board(self) -> Board:
        return self._game_board

    def get_move_count(self) -> int:
        return self._move_count

    def get_weighted_score(self) -> float:
        return self._weighted_score

    def get_score(self) -> int:
        return self._game_board.get_score()

    def display(self):
        print(self._game_board.get_board())
        print("current total score: %d" % self._game_board.get_score())
        print("current move count: %d" % self._move_count)
        print("current weighed score : %f" % self.get_weighted_score())
        print("========================================================")

    def get_new_pos(self) -> (int, int):
        return self._game_board.get_new_pos()

    # def test_board(self, board):
    #     self._game_board.test_board(board)

    def do_action(self, action: str):
        """
        First, extract lines according to user's input, within each line holds the coordinate of each tile
        Then, move and merge tiles
        :param action:
        :return:
        """
        lines = self._get_lines(action=action)

        self._game_board.merge_tile(lines=lines, merge_to_left=Action.left_direction(action))

        self._move_count += 1

        self._weighted_score = float(self._game_board.get_score()) / math.log(float(self._move_count+1), 2.)

    def _get_lines(self, action: str) -> list:
        lines = []
        if action in [Action.left.get_value(), Action.right.get_value()]:
            lines = self._get_row_lines(indexes=self._board_indexes)
        elif action in [Action.up.get_value(), Action.down.get_value()]:
            # a vertical operation, transpose the board, then call _get_row_lines
            index_trans = np.transpose(self._board_indexes)
            lines = self._get_row_lines(indexes=index_trans)
        elif action in [Action.upLeft.get_value(), Action.downRight.get_value()]:
            lines = self._get_diagonal_lines(indexes=self._board_indexes)
        else:
            # a forward slash operation, flip the board vertically and call _get_diagonal_lines
            index_flip = np.fliplr(self._board_indexes)
            lines = self._get_diagonal_lines(indexes=index_flip)
        return lines

    def _get_row_lines(self, indexes: np.ndarray) -> list:
        lines = []
        # a horizontal operation, get coordinate of each tile from each row
        for i in range(indexes.shape[0]):
            lines.append(indexes[i, :])
        return lines

    def _get_diagonal_lines(self, indexes: np.ndarray) -> list:
        # get the diagonal of the board first
        lines = [np.diagonal(indexes)]
        for i in range(1, indexes.shape[0] - 1):
            # shrink the board to the down left corner by 1 tile, then get its diagonal
            lines.append(np.diagonal(indexes[i:, :(indexes.shape[1] - i)]))
            # shrink the board to the up right corner by 1 tile, then get its diagonal
            lines.append(np.diagonal(indexes[:(indexes.shape[1] - i), i:]))
        return lines

    def valid_action(self, action: str) -> bool:
        if action in self.valid_actions():
            return True
        return False

    def valid_actions(self) -> list:
        valid_actions = []
        for act in Action.__members__.values():
            lines = self._get_lines(action=act.get_value())
            if self._game_board.movable(lines=lines, to_left=Action.left_direction(act.get_value())):
                valid_actions.append(act.get_value())
        return valid_actions

    @property
    def game_over(self) -> (bool, bool):
        if np.any(self._game_board.get_board() == self._goal):
            return True, True
        if len(self.valid_actions()) == 0:
            self._weighted_score = -1
            return True, False
        return False, False

