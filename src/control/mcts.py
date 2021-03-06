from src.game.game import Game
from src.control.play import PlayInterface
import copy
import random
import time


class MCT:
    def __init__(self, game: Game):
        self._root_state = game
        self._move_count = 0
        self._avg_score = 0.0
        self._parent = None
        self._children = []

    def get_game_state(self) -> Game:
        return self._root_state

    def get_children(self) -> list:
        return self._children

    def append_child(self):
        pass


class MCTS(PlayInterface):
    def __init__(self):
        pass

    def _roll_out(self, root: MCT, depth: int = 20) -> list:
        game_over, win = root.get_game_state().game_over
        if game_over:
            if win:
                pass
            else:
                pass
        children = []
        if depth == 0:
            children = root.get_children()


    def get_move(self):
        pass

    def _get_children(self, root: MCT):
        valid_actions = root.get_game_state().valid_actions()

    def play(self, game: Game) -> str:
        input("Press enter to continue:")
        start = time.time()
        action = self._make_move(game)
        end = time.time()
        time_elapse = end - start
        print("MCTS timing: time consumption of determined current move is %s second" % str(time_elapse))
        return action

    def _make_move(self, game:Game):
        total_simulations = 20
        games_per_move = total_simulations // 4

        valid_actions = game.valid_actions()

        scores = self._calculate_random(game, valid_actions, games_per_move)

        best_move_idx = scores.index(max(scores))
        best_move = valid_actions[best_move_idx]
        return best_move

    def _calculate_random(self, game: Game, valid_actions: list, games_per_move: int):

        scores = [0] * len(valid_actions)

        for i, mv in enumerate(valid_actions):
            for _ in range(games_per_move):
                scores[i] += self._simulate_run(mv, i, game)
        return scores

    def _simulate_run(self, move, i, game:Game,  max_depth=None):
        simulation = copy.deepcopy(game)
        if simulation.valid_action(move):
            simulation.do_action(action=move)
            moves = 0
            while not game.game_over[0]:
                if max_depth:
                    if moves >= max_depth:
                        break
                valid_actions = simulation.valid_actions()
                if not valid_actions:
                    break
                m = random.choice(valid_actions)
                simulation.do_action(m)
                moves += 1

        return simulation.get_weighted_score()
