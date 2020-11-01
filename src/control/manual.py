from src.game.game import Game


def play():
    game = Game()
    game.display()
    while not game.game_over:
        action = input("Please input a move: ")
        if not game.valid_action(action=action):
            print("Action Invalid!! Game board not updated!!!")
            continue
        game.do_action(action=action)
        print("Newly generated tile at: %s" % str(game.get_new_pos()))
        game.display()
    print("Final weighted score is : %d" % game.get_weighted_score())
