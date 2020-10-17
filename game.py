from actions import Action
from board import Board
import numpy as np


class Game:
    def __init__(self):
        self._game_board = Board()
        self._board_indedxes = self._game_board_indexes(self._game_board.get_size())
        self._goal = 2048

    def _game_board_indexes(self, size):
        board_index = np.ndarray(shape=(size, size), dtype=object)
        for r in range(board_index.shape[0]):
            for c in range(board_index.shape[1]):
                board_index[r, c] = (r, c)
        return board_index

    def display(self):
        print(self._game_board.get_board())

    def update_state(self, action):
        """
        First, extract lines according to user's input, within each line holds the coordinate of each tile
        Then, move and merge tiles
        :param action:
        :return:
        """
        lines = []
        if action == Action.left or action == Action.right:
            lines = self._get_row_lines(indexes=self._board_indedxes)
        elif action == Action.up or action == Action.down:
            # a vertical operation, transpose the board, then call _get_row_lines
            index_trans = np.transpose(self._board_indedxes)
            lines = self._get_row_lines(indexes=index_trans)
        elif action == Action.upLeft or action == Action.downLeft:
            lines = self._get_diagonal_lines(indexes=self._board_indedxes)
        else:
            # a forward slash operation, flip the board vertically and call _get_diagonal_lines
            index_flip = np.fliplr(self._board_indedxes)
            lines = self._get_diagonal_lines(indexes=index_flip)
        if action in [Action.up, Action.left, Action.upLeft, Action.upRight]:
            self._game_board.merge_tile(lines=lines, merge_to_left=True)
        else:
            self._game_board.merge_tile(lines=lines, merge_to_left=False)

        if action in [Action.left, Action.up, Action.upRight, Action.upLeft]:
            self._game_board.merge_tile(lines=lines, merge_to_left=True)
        else:
            self._game_board.merge_tile(lines=lines, merge_to_left=False)

    def _get_row_lines(self, indexes):
        lines = []
        # a horizontal operation, get coordinate of each tile from each row
        for i in range(indexes.shape[0]):
            lines.append(indexes[i, :])
        return lines

    def _get_diagonal_lines(self, indexes):
        # get the diagonal of the board first
        lines = [np.diagonal(indexes)]
        for i in range(1, indexes.shape[0] - 2):
            # shrink the board to the down left corner by 1 tile, then get its diagonal
            lines.append(np.diagonal(indexes[i:, :(indexes.shape[1] - i)]))
            # shrink the board to the up right corner by 1 tile, then get its diagonal
            lines.append(np.diagonal(indexes[:(indexes.shape[1] - i), i:]))
        return lines

    def valid_action(self, action):
        return False

    def _valid_actions(self):
        return 1

    @property
    def game_over(self):
        if self._valid_actions() == 0:
            print("you loose!!!")
            return True
        if np.any(self._game_board.get_board() == self._goal):
            print("you win !!!")
            return True
        return False


if __name__ == '__main__':
    game = Game()
    move_count = 0
    game.display()
    while not game.game_over:
        action = input("Please input a move: ")
        if not game.valid_action(action=action):
            continue
        # @TODO update game board
        game.update_state(action=action)
        game.display()
