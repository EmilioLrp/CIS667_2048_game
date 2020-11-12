import test.game_test as gtest
from src.control.manual import Manual
from src.control.mcts_new import MCTSNew
from src.control.uniform_random import URand
from src.control.play import PlayInterface
from src.game.game import Game
import sys
import numpy as np


def play(mode: PlayInterface):
    record_sub = False
    game = Game()
    game.init_board(size=4, goal=2048)
    game.display()
    while not game.game_over[0]:
        action = mode.play(game=game)
        if not game.valid_action(action=action):
            print("Action Invalid!! Game board not updated!!!")
            continue
        game.do_action(action=action)
        print("Newly generated tile at: %s" % str(game.get_new_pos()))
        # game.display()
        if sub_problem(1024, game) and not record_sub:
            record_sub = True
            with open(file='1024_result.txt', mode='a') as file_1:
                msg = "total score: %s, move count: %s, weighted: %s\n" % (game.get_board().get_score(), game.get_move_count(), game.get_weighted_score())
                file_1.write(msg)

        elif sub_problem(2048, game):
            with open(file='2048_result.txt', mode='a') as file_2:
                msg = "total score: %s, move count: %s, weighted: %s\n" % (game.get_board().get_score(), game.get_move_count(), game.get_weighted_score())
                file_2.write(msg)
    if not game.game_over[1]:
        if np.max(game.get_board().get_board()) < 1024:
            with open(file='1024_result.txt', mode='a') as file_1:
                msg = "total score: %s, move count: %s, weighted: %s\n" % (game.get_board().get_score(), game.get_move_count(), game.get_weighted_score())
                file_1.write(msg)

        if np.max(game.get_board().get_board()) < 2048:
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

    for i in range(20):
        play(mode=action_mode)
        with open(file="log.log", mode='a') as log:
            log.write("iteration %s has complete" % str(i))
