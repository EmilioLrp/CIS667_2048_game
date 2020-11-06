from src.game.game import Game


class MCT:
    def __init__(self, game_board):
        self._board = game_board
        self._move_count = 0
        self._avg_score = 0.0
        self._parent = None
        self._children = None


class MCTS:
    def __init__(self):

        pass

    def _get_child(self):
        pass

    def _roll_out(self, depth=20):
        pass

    def get_move(self):
        pass
