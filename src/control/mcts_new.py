from src.game.game import Game
from src.control.play import PlayInterface
import copy
import numpy as np
import random
import time
import sys

sys.setrecursionlimit(4000)


class MCT(object):
    def __init__(self, state: Game = None):
        self._state = state
        # self._action = action
        self._move_count = 0
        self._avg_score = 0.0
        self._total_score = 0.0
        self._parent = None
        self._children = []
        self._score = 0.0

    #
    def get_game_state(self) -> Game:
        return self._state

    # def get_action(self):
    #     return self._action

    def get_children(self) -> list:
        return self._children

    def set_parent(self, parent):
        self._parent = parent

    def set_child(self, child):
        if not self.child_exists(child.get_game_state()):
            self._children.append(child)
            return child
        else:
            child_dict = dict(zip([c.get_action() for c in self._children], self._children))
            return child_dict[child.get_action()]

    def child_exists(self, state: np.ndarray) -> bool:
        child_state = [child.get_game_state for child in self._children]
        if state in child_state:
            return True
        return False

    def get_score(self) -> float:
        return self._score

    def get_total_score(self):
        return self._total_score

    def update_total_score(self, score):
        self._total_score = score

    def set_score(self, score):
        self._score = float(score)

    def inc_move_count(self):
        self._move_count += 1

    def get_move_count(self) -> int:
        return self._move_count

    def update_scores(self, score):
        self._avg_score = float(score) / float(self._move_count)


class MCTSNew(PlayInterface):
    def __init__(self):
        pass

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
        all_actions = state.valid_actions()
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

    def play(self, game:Game):
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
