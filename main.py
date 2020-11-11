import test.game_test as gtest
from src.control.manual import Manual
from src.control.mcts import MCTS
from src.control.play import PlayInterface
from src.game.game import Game
import sys


def unit_test():
    gtest.start_test()


def play(mode: PlayInterface):
    game = Game()
    game.display()
    game_over, win = game.game_over
    size = input("Please input a board size: ")
    game.get_board().set_size(int(size))
    while not game_over:
        action = mode.play(game=game)
        if not game.valid_action(action=action):
            print("Action Invalid!! Game board not updated!!!")
            continue
        game.do_action(action=action)
        print("Newly generated tile at: %s" % str(game.get_new_pos()))
        game.display()
    print("Final weighted score is : %d" % game.get_weighted_score())


if __name__ == '__main__':
    action_mode = None
    while True:
        mode = input(
            "please input a mode to start the game(m for manual, mcts for tree search, ml for machine learning): ")
        if mode == "m":
            action_mode = Manual()
            break
        elif mode == "mcts":
            action_mode = MCTS()
            break
        # elif mode == "ml":
        #     break
        elif mode == "test":
            unit_test()
            sys.exit()
        else:
            print("Invalid!!! please input again!!!!")

    play(mode=action_mode)
