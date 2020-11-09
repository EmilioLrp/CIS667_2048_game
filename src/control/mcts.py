from src.game.game import Game
from src.control.play import PlayInterface
import copy
import random


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

    def play(self, game: Game):
        # create a deep copy of the current game state
        return self._make_move(game)

    def _make_move(self, game:Game):
        total_simulations = 20
        games_per_move = total_simulations // 4

        valid_actions = game.valid_actions()

        self.total_move_scores = [0] * len(valid_actions)
        self.total_move_moves = [0] * len(valid_actions)
        self.total_games_done = 0

        #for i, mv in enumerate(['2','4','6','8']):
        print(game.valid_actions())
        for i, mv in enumerate(valid_actions):
            for _ in range(games_per_move):
                self._simulate_run(mv, i, game) 

        best_move_idx = self.total_move_scores.index(max(self.total_move_scores))
        best_move = valid_actions[best_move_idx]
        return best_move


    def _simulate_run(self, move, i, game:Game):
        simulation = copy.deepcopy(game)

        if simulation.valid_action(move):
            simulation.do_action(action=move)
            moves = 0
            while not game.game_over[0]:
                # TODO
                valid_actions = simulation.valid_actions()
                #print(valid_actions)
                if not valid_actions:
                    break
                m = random.choice(valid_actions)
                simulation.do_action(m)
                moves += 1
            self.total_move_scores[i] += simulation.get_weighted_score() * moves
            self.total_move_moves[i] += moves

        self.total_games_done += 1
        return

    def _filter_valid(self, actions):
        s = set(actions)
        s.discard("1")
        s.discard("3")
        s.discard("7")
        s.discard("9")
        return list(s)


        
        






