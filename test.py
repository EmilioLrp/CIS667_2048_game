import test.game_test as gtest
from src.control.manual import Manual
from src.control.mcts_new import MCTSNew
from src.control.uniform_random import URand
from src.control.play import PlayInterface
from src.game.game import Game
import sys
import numpy as np
import time


def play(mode: PlayInterface, size, goal, mode_name):
    record_sub = False
    game = Game()
    game.init_board(size=size, goal=goal)
    game.display()
    node_count = 0
    file_name = "%d_%d_%s_result.txt" % (size, goal, mode_name)
    while not game.game_over[0]:
        if isinstance(mode, URand):
            action, nodes = mode.play_game(game=game)
        else:
            action, nodes = mode.play(game=game)
        if not game.valid_action(action=action):
            print("Action Invalid!! Game board not updated!!!")
            continue
        node_count += nodes
        game.do_action(action=action)
        print("Newly generated tile at: %s" % str(game.get_new_pos()))
        game.display()
        if sub_problem(goal, game) and not record_sub:
            record_sub = True
            with open(file=file_name, mode='a') as file_1:
                msg = "total score: %s, move count: %s, weighted: %s, node count: %s\n" % \
                      (game.get_board().get_score(), game.get_move_count(), game.get_weighted_score(), node_count)
                file_1.write(msg)
                file_1.flush()
    if not game.game_over[1]:
        if np.max(game.get_board().get_board()) < goal:
            with open(file=file_name, mode='a') as file_1:
                msg = "total score: %s, move count: %s, weighted: %s, node_count: %s\n" % \
                      (game.get_board().get_score(), game.get_move_count(), game.get_weighted_score(), node_count)
                file_1.write(msg)
                file_1.flush()

    print("Final weighted score is : %d" % game.get_weighted_score())
    print("Total nodes generated: %d" % node_count)


def sub_problem(goal, game):
    if np.any(game._game_board.get_board() == goal):
        return True
    return False


if __name__ == '__main__':
    # start = time.time()
    action_mode = URand()

    rand_modes = [(3, 128, "rand"), (3, 256, "rand"), (3, 512, "rand"), (4, 1024, "rand"), (4, 2048, "rand")]
    mcts_modes = [(3, 128, "mcts"), (3, 256, "mcts"), (3, 512, "mcts"), (4, 1024, "mcts"), (4, 2048, "mcts")]

    # for size, goal, name in rand_modes:
    #     for i in range(100):
    #         play(mode=action_mode, size=size, goal=goal, mode_name=name)

    action_mode = MCTSNew()
    for size, goal, name in mcts_modes:
        for i in range(20):
            play(mode=action_mode, size=size, goal=goal, mode_name=name)
            # with open(file="log.log", mode='a') as log:
            #     log.write("iteration %s has complete" % str(i))
    # print(time.time() - start)