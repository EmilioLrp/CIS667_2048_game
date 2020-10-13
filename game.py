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

    def __crush_line(self, line):
        out = []
        first = None
        for i in range(len(line)):
            if line[i] == 0:
                continue
            if not first:
                first = line[i]
            else:
                if line[i] == first:
                    out.append(first * 2)
                    first = None
                else:
                    out.append(first)
                    first = line[i]
        if first:
            out.append(first)
        if len(out) < len(line):
            out += [0] * (len(line) - len(out))
        return out

    def left(self):
        valid = False
        for i in range(len(self._game_board)):
            move = self.__crush_line(self._game_board[i])
            if not np.array_equal(self._game_board[i], move):
                self._game_board[i] = move
                valid = True
        if valid:
            self._generate_rand_tile()
        return self._game_board, valid

    def right(self):
        valid = False
        for i in range(len(self._game_board)):
            move = self.__crush_line(self._game_board[i][::-1])[::-1]
            if not np.array_equal(self._game_board[i], move):
                self._game_board[i] = move
                valid = True
        if valid:
            self._generate_rand_tile()
        return self._game_board, valid

    def up(self):
        valid = False
        for i in range(len(self._game_board)):
            move = self.__crush_line(self._game_board[:,i])
            if not np.array_equal(self._game_board[:,i], move):
                self._game_board[:,i] = move
                valid = True
        if valid:
            self._generate_rand_tile()
        return self._game_board, valid

    def down(self):
        valid = False
        for i in range(len(self._game_board)):
            move = self.__crush_line(self._game_board[:,i][::-1])[::-1]
            if not np.array_equal(self._game_board[:,i], move):
                self._game_board[:,i] = move
                valid = True
        if valid:
            self._generate_rand_tile()
        return self._game_board, valid

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
    #moves = ['l','l','r','u']
    while True:
        m = input("Please input a move: ")
        valid = True
        if m == 'l':
            _, valid = board.left()
        elif m == 'r':
            _, valid = board.right()
        elif m == 'u':
            _, valid = board.up()
        elif m == 'd':
            _, valid = board.down()
        if not valid:
            print("Not a valid move")
        board.display()


    # while True:
    #     move = board.play_move()
    #     move_count += 1
    #     board.update_state(move=move)
    #     board.display()
    #     if board.game_over():
    #         break
    # print("Total move used: %d" % move_count)
