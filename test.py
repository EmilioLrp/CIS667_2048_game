import test.game_test as gtest
from src.control.manual import Manual
from src.control.mcts_new import MCTSNew
from src.control.uniform_random import URand
from src.control.play import PlayInterface
from src.game.game import Game
import sys
import numpy as np


def play(mode: PlayInterface):
    game = Game()
    game.display()
    while not game.game_over[0]:
        action = mode.play(game=game)
        if not game.valid_action(action=action):
            print("Action Invalid!! Game board not updated!!!")
            continue
        game.do_action(action=action)
        print("Newly generated tile at: %s" % str(game.get_new_pos()))
        # game.display()
        if sub_problem(1024, game):
            with open(file='1024_result.txt', mode='a') as file_1:
                msg = "total score: %s, move count: %s, weighted: %s\n" % (game.get_board().get_score(), game.get_move_count(), game.get_weighted_score())
                file_1.write(msg)

        elif sub_problem(2048, game):
            with open(file='2048_result.txt', mode='a') as file_2:
                msg = "total score: %s, move count: %s, weighted: %s\n" % (game.get_board().get_score(), game.get_move_count(), game.get_weighted_score())
                file_2.write(msg)

    print("Final weighted score is : %d" % game.get_weighted_score())


def sub_problem(goal, game):
    if np.any(game._game_board.get_board() == goal):
        return True
    return False


if __name__ == '__main__':
    action_mode = MCTSNew()

    play(mode=action_mode)
