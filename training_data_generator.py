from src.control.mcts_new import MCTSNew, MCT
from src.game.game import Game, Action
import os
import random
import copy
import numpy as np
import pickle as pk


# def training_data_generator():
#     pass
#
#
# def testing_data_generator():
#     pass


def data_generator(size, goal):
    mcts = MCTSNew()

    file_name = os.path.dirname(os.path.abspath(__file__)) + "/data/board_size_%d_goal_%d_train.dat" % (size, goal)
    # list of game states
    state_data = []
    # list of desired output after softmax
    desired_output = []
    # count = 100
    while len(state_data) < 4000:
        game = Game()
        game.init_board(size=size, goal=goal)
        while not game.game_over[0]:
            # game_over, win = game.game_over
            # if game_over:
            #     break
            state_data.append(game.get_board().get_board())
            actions_dict = dict([(act.get_value(), 0.) for act in Action.__members__.values()])
            actions = game.valid_actions()

            action_child_pair = {}
            for move in actions:
                state = copy.deepcopy(game)
                root_child = MCT(state=state)
                root_child, _ = mcts.roll_out(root=root_child, state=state, depth=None)
                actions_dict[
                    move] = root_child.get_game_state().get_weighted_score() + 2  # for normalizing -1 to 1, differentiating 0
                action_child_pair[move] = root_child
                max_score = np.max([child.get_score() for child in action_child_pair.values()])
            candidates = [action for action, node in action_child_pair.items() if node.get_score() == max_score]

            action_scores = np.array(list(actions_dict.values()))
            softmax_scores = [score / np.sum(action_scores) for score in action_scores]
            desired_output.append(softmax_scores)

            game.do_action(random.choice(candidates))
            # count -= 1

    with open(file_name, "wb") as f:
        pk.dump((state_data, desired_output), f)


if __name__ == '__main__':

    game_sizes = [(3, 128), (3, 256), (4, 512), (4, 1024), (4, 2048)]
    for size, goal in game_sizes:
        print("Starting to generate data for game size %d, goal%d" % (size, goal))
        data_generator(size, goal)
        print("Complete generating data")
