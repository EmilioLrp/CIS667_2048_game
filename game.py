from actions import Action
from board import Board
import numpy as np


class Game:
    def __init__(self):
        self._game_board = Board()
        self._board_indexes = Game._game_board_indexes(self._game_board.get_size())
        self._goal = 2048

    @classmethod
    def _game_board_indexes(cls, size):
        board_index = np.ndarray(shape=(size, size), dtype=object)
        for r in range(board_index.shape[0]):
            for c in range(board_index.shape[1]):
                board_index[r, c] = (r, c)
        return board_index

    def display(self):
        print(self._game_board.get_board())
        print("current score: %d" % self._game_board.get_score())

    def get_new_pos(self):
        return self._game_board.get_new_pos()

    # def test_board(self, board):
    #     self._game_board.test_board(board)

    def do_action(self, action):
        """
        First, extract lines according to user's input, within each line holds the coordinate of each tile
        Then, move and merge tiles
        :param action:
        :return:
        """
        lines = self._get_lines(action=action)

        self._game_board.merge_tile(lines=lines, merge_to_left=Action.left_direction(action))

    def _get_lines(self, action):
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

    def _get_row_lines(self, indexes):
        lines = []
        # a horizontal operation, get coordinate of each tile from each row
        for i in range(indexes.shape[0]):
            lines.append(indexes[i, :])
        return lines

    def _get_diagonal_lines(self, indexes):
        # get the diagonal of the board first
        lines = [np.diagonal(indexes)]
        for i in range(1, indexes.shape[0] - 1):
            # shrink the board to the down left corner by 1 tile, then get its diagonal
            lines.append(np.diagonal(indexes[i:, :(indexes.shape[1] - i)]))
            # shrink the board to the up right corner by 1 tile, then get its diagonal
            lines.append(np.diagonal(indexes[:(indexes.shape[1] - i), i:]))
        return lines

    def valid_action(self, action):
        if action in self._valid_actions():
            return True
        return False

    def _valid_actions(self):
        valid_actions = []
        for act in Action.__members__.values():
            lines = self._get_lines(action=act.get_value())
            if self._game_board.movable(lines=lines, to_left=Action.left_direction(act.get_value())):
                valid_actions.append(act.get_value())
        return valid_actions

    @property
    def game_over(self):
        if len(self._valid_actions()) == 0:
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
            print("Action Invalid!! Game board not updated!!!")
            continue
        game.do_action(action=action)
        move_count += 1
        game.display()
        print("Newly generated tile at: %s" % str(game.get_new_pos()))
    print("Total move count to the end of game: %d" % move_count)
    # board = np.zeros((4, 4), dtype=int)
    # board[0, :] = [128, 512, 128, 64]
    # board[1, :] = [64, 32, 8, 4]
    # board[2, :] = [16, 2, 0, 0]
    # board[3, :] = [2, 0, 0, 2]
    # game.test_board(board)
    # game.display()
    # action = input("action:")
    # if not game.valid_action(action=action):
    #     print("Action Invalid!! Game board not updated!!!")
    # else:
    #     game.do_action(action=action)
    #     game.display()
