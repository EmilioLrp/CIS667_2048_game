import copy
import operator
import os
import random
import sys
import time

import numpy as np
import torch as tr

from src.control.mcts_new import MCT
from src.control.play import PlayInterface
from src.game.actions import Action
from src.game.game import Game


sys.setrecursionlimit(4000)


class MCTS_NN(PlayInterface):
    def __init__(self, game_size, game_goal, mode_dir='rliu02'):
        self._size = game_size
        self._goal = game_goal
        self._model = self._load_nn(mode_dir)
        self._action = [act.get_value() for act in Action.__members__.values()]

    def _load_nn(self, mode_dir):
        if mode_dir == 'rliu02':
            from src.model.conv_nn_rliu02 import NNModel
        elif mode_dir == 'dguo13':
            from src.model.conv_nn_rliu02 import NNModel
        else:
            from src.model.conv_nn_rliu02 import NNModel
        model = NNModel(self._size)
        model_file = os.path.abspath(os.getcwd()) + "/model/%s/board_size_%d_goal_%d_model.mod" % (mode_dir, self._size, self._goal)
        model.load_state_dict(tr.load(model_file))
        return model

    def roll_out(self, root: MCT, state: Game, depth=5) -> (MCT, int):
        root.inc_move_count()
        game_over, win = state.game_over
        if depth is None:
            if game_over:
                root.update_total_score(score=state.get_weighted_score())
                return root, 1
        else:
            if game_over or depth <= 0:
                root.update_total_score(score=state.get_weighted_score())
                return root, 1

        child_depth = None
        if depth:
            child_depth = depth - 1
        all_actions = self._action_selection(state=state, size=self._size)
        nodes = len(all_actions)
        child_states = []
        states_score = []
        for action in all_actions:
            child_state = copy.deepcopy(state)
            child_state.do_action(action)
            child_states.append(child_state)
            states_score.append(child_state.get_weighted_score())
        max_indices = self.choose_child(child_states, states_score)
        child_id = random.choice(max_indices)
        child = MCT(child_states[child_id])
        child, node_count = self.roll_out(root=child, state=child_states[child_id], depth=child_depth)
        root.set_child(child)
        nodes += node_count
        root.update_total_score(root.get_total_score() + child.get_total_score())
        self._calculate_score(root)
        return root, nodes

    def _action_selection(self, state, size):
        all_act = state.valid_actions()
        x = tr.tensor(state.get_board().get_board()).reshape((1, 1, size, size)).float()
        model_out = self._model.forward(x).detach().numpy()[0]
        model_map = dict(list(zip(self._action, model_out)))
        # filter out impossibilities by the model
        model_map = {x: y for x, y in model_map.items() if y != 0}
        # filter out remain actions that is not valid
        model_map = {x: y for x, y in model_map.items() if all_act.__contains__(x)}
        model_act = []
        for _ in range(3):
            if not bool(model_map):
                break
            max_move = max(model_map.items(), key=operator.itemgetter(1))[0]
            model_act.append(max_move)
            del model_map[max_move]
        if len(model_act) > 0:
            model_act = [str(act) for act in model_act]
            return model_act
        else:
            return all_act

    def play(self, game: Game):
        input("Press Enter to continue:")
        return self.play_auto(game)

    def play_auto(self, game: Game) -> (str, int):
        start = time.time()
        move, nodes = self._play(game)
        end = time.time()
        print("current node is %s" % str(nodes))
        print("roll out time: %s" % str(end - start))
        return move, nodes

    def _play(self, game: Game):
        # roll out will be based on the deep copy of the original state
        actions = game.valid_actions()
        action_child_pair = {}
        node_count = 0
        for move in actions:
            # create a deep copy of the current game state
            game_copy = copy.deepcopy(game)
            game_copy.do_action(action=move)
            root_child = MCT(state=game_copy)
            for _ in range(1):
                root_child, nodes = self.roll_out(root=root_child, state=game_copy, depth=10)
                node_count += nodes
            action_child_pair[move] = root_child
            max_score = np.max([child.get_score() for child in action_child_pair.values()])
        candidates = [action for action, node in action_child_pair.items() if node.get_score() == max_score]
        return random.choice(candidates), node_count

    def _calculate_score(self, node: MCT):
        # move_count = node.get_move_count()
        # node.set_score(-move_count)
        node.set_score(node.get_total_score())

    def choose_child(self, child_states, scores):
        max_score = np.max(scores)
        positions = np.concatenate(np.argwhere(np.array(scores) == max_score), axis=0)
        return positions
