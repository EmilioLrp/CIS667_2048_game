import test.game_test as gtest
from src.control.manual import Manual
from src.control.mcts_new import MCTSNew
from src.control.uniform_random import URand
from src.control.play import PlayInterface
from src.control.mcts_nn import MCTS_NN
from src.game.game import Game
import sys

move_mapping = {
    '1': 'Lower left',
    '2': 'Down',
    '3': 'Lower right',
    '4': 'Left',
    '6': 'Right',
    '7': 'Upper left',
    '8': 'Up',
    '9': 'Upper right',
}


def unit_test():
    gtest.start_test()


def play(size, goal, mode: PlayInterface):
    game = Game()
    game.init_board(size=int(size), goal=int(goal))
    game.display()
    while True:
        game_over, win = game.game_over
        if game_over:
            break
        action, count = mode.play(game=game)
        if not game.valid_action(action=action):
            print("Action Invalid!! Game board not updated!!!")
            continue
        # print("Time elapsed: {time} second(s), Move selected: {move} ({move_mapping})".format(
        #     time=end - start, move=action, move_mapping=move_mapping[action]
        #     ))
        print("Move that has been decided: %s" % move_mapping[action])
        game.do_action(action=action)
        print("Newly generated tile at: %s" % str(game.get_new_pos()))
        game.display()
    print("Final weighted score is : %d" % game.get_weighted_score())
    if game.game_over[1]:
        print("you win !!!")
    else:
        print("you loose!!!")


def get_customed_size_board():
    choice = input("please select a game question instance:\n"
                   "a: 3*3, 128\n"
                   "b: 3*3, 256\n"
                   "c: 4*4, 512\n"
                   "d: 4*4, 1024\n"
                   "e: 4*4, 2048\n")
    if choice == "a":
        return 3, 128
    elif choice == "b":
        return 3, 256
    elif choice == "c":
        return 4, 512
    elif choice == "d":
        return 4, 1024
    elif choice == "e":
        return 4, 2048
    else:
        raise BaseException


if __name__ == '__main__':
    action_mode = None
    size, goal = get_customed_size_board()
    while True:
        mode = input(
            "please input a mode to start the game:\n" +
            "[human] for manual play\n" +
            "[baseline] for auto play based on universal random selection\n"+
            "[tree] for auto play based on tree search\n"+
            "[tree-nn] for auto play based on tree search + NN\n")
        if mode == "human":
            action_mode = Manual()
            break
        elif mode == "tree":
            action_mode = MCTSNew()
            break
        elif mode == "tree-nn":
            action_mode = MCTS_NN(game_size=size)
            break
        elif mode == "baseline":
            action_mode = URand()
            break
        elif mode == "test":
            unit_test()
            sys.exit()
        else:
            print("Invalid!!! please input again!!!!")

    play(size=size, goal=goal, mode=action_mode)
