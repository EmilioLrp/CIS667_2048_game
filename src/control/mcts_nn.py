from src.game.game import Game
from src.control.play import PlayInterface
from src.control.mcts_new import MCT
from src.control.conv_nn import NNModel
from src.game.actions import Action
import torch as tr
import copy
import numpy as np
import random
import time
import os
import sys
import operator

sys.setrecursionlimit(4000)


class MCTS_NN(PlayInterface):
    def __init__(self, game_size):
        self._size = game_size
        self._model = self._load_nn()
        self._action = [act.value() for act in Action.__members__.values()]

    def _load_nn(self):
        model = NNModel(self._size)
        model_file = os.path.dirname("main.py") + "/model/board_size_%d_model.mod" % self._size
        model.load_state_dict(tr.load(model_file))

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
        all_actions = self._action_selection(state=state)
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

    def _action_selection(self, state):
        all_act = state.valid_actions()
        model_out = self._model(tr.tensor(state.get_board().get_board())).reshape(
            (1, 1, self._size, self._size)).float()
        model_map = dict(list(zip(range(len(model_out)), model_out)))
        model_map = {x: y for x, y in model_map.items() if y != 0}
        model_act = []
        for _ in range(3):
            if bool(model_map):
                break
            max_move = max(model_map.items(), key=operator.itemgetter(1))
            model_act.append(max_move)
            del model_map[max_move]
        moves = [self._action[i] for i in model_act]
        result = [act for act in moves if act in all_act]
        if bool(result):
            return all_act
        else:
            return result


    def play(self, game: Game) -> (str, int):
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
