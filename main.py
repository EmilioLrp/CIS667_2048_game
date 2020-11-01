from src.control import manual
import test.game_test as gtest


def manual_play():
    manual.play()


def unit_test():
    gtest.start_test()


if __name__ == '__main__':
    while True:
        mode = input(
            "please input a mode to start the game(m for manual, mcts for tree search, ml for machine learning): ")
        if mode == "m":
            manual_play()
            break
        elif mode == "mcts":
            break
        elif mode == "ml":
            break
        elif mode == "test":
            unit_test()
            break
        else:
            print("Invalid!!! please input again!!!!")
