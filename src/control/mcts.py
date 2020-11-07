from src.game.game import Game
from src.control.play import PlayInterface
import copy


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
        game_copy = copy.deepcopy(game)
        actions = game_copy.valid_actions()
        # roll out will be based on the deep copy of the original state
        root = MCT(game=game_copy)
        children = self._roll_out(root=root, depth=20)
        pass
