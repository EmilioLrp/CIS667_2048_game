from src.game.game import Game
from src.control.play import PlayInterface
import copy
import numpy as np
import random
import time


class MCT(object):
    def __init__(self, action: str = None):
        # self._root_state = game
        self._action = action
        self._move_count = 0
        self._avg_score = 0.0
        self._total_score = 0.0
        self._parent = None
        self._children = []
        self._score = 0.0

    #
    # def get_game_state(self) -> Game:
    #     return self._root_state

    def get_action(self):
        return self._action

    def get_children(self) -> list:
        return self._children

    def set_parent(self, parent):
        self._parent = parent

    def set_child(self, child):
        if not self.child_exists(child.get_action):
            self._children.append(child)
            return child
        else:
            child_dict = dict(zip([c.get_action() for c in self._children], self._children))
            return child_dict[child.get_action()]

    def child_exists(self, action: str) -> bool:
        child_act = [child.get_action for child in self._children]
        if action in child_act:
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

    def _roll_out(self, root: MCT, state: Game, depth: int = 5) -> MCT:
        root.inc_move_count()
        game_over, win = state.game_over
        # game_over, win = root.get_game_state().game_over
        # root.inc_move_count()
        if game_over or depth == 0:
            root.update_total_score(score=state.get_weighted_score())
            return root
        all_actions = state.valid_actions()
        actions = random.sample(all_actions, min(4, len(all_actions)))
        for move in actions:
            child = MCT(move)
            child_state = copy.deepcopy(state)
            child_state.do_action(move)
            child = root.set_child(child)
            child = self._roll_out(root=child, state=child_state, depth=depth - 1)
            root.update_total_score(root.get_total_score() + child.get_total_score())
            self._calculate_score(root)
        return root

    def play(self, game: Game) -> str:
        start = time.time()
        move = self._play(game)
        end = time.time()
        print("roll out time: %s" % str(end - start))
        return move

    def _play(self, game:Game):
        # roll out will be based on the deep copy of the original state
        actions = game.valid_actions()
        action_child_pair = {}
        for move in actions:
            # create a deep copy of the current game state
            game_copy = copy.deepcopy(game)
            game_copy.do_action(action=move)
            root_child = MCT(action=move)
            for _ in range(1):
                root_child = self._roll_out(root=root_child, state=game_copy, depth=5)
            action_child_pair[move] = root_child
        max_score = np.max([child.get_score() for child in action_child_pair.values()])
        candidates = [action for action, node in action_child_pair.items() if node.get_score() == max_score]
        return random.choice(candidates)

    def _calculate_score(self, node: MCT):
        # move_count = node.get_move_count()
        # node.set_score(-move_count)
        node.set_score(node.get_total_score())
