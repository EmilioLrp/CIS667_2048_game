from src.control import manual


def manual_play():
    manual.play()


if __name__ == '__main__':
    while True:
        mode = input(
            "please input a mode to start the game(m for manual, mcts for tree search, ml for machine learning): ")
        if mode == "manual":
            manual_play()
            break
        elif mode == "mcts":
            break
        elif mode == "ml":
            break
        else:
            print("Invalid!!! please input again!!!!")
