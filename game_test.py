from game import Game
from actions import Action
import unittest as ut
import numpy as np



class GameTestCase(ut.TestCase):
    
    def print_test_case(self, expected, actual):
        # helper method to print out failed test cases
        print("%s failed:" % ip.currentframe().f_back.f_code.co_name)
        print("expected:")
        print(expected)
        print("actual:")
        print(actual)
    
    def test_single(self):
        game = Game()
        game._game_board._game_board = np.array(
            [[0, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 4, 0],
            [0, 0, 0, 0]]
        )
        game.do_action("4")
        x, y = game.get_new_pos()
        expected = [
            [0, 0, 0, 0],
            [4, 0, 0, 0],
            [4, 0, 0, 0],
            [0, 0, 0, 0]]
        expected[x][y] = 2
        print('\n',game._game_board._game_board, '\n\n', np.array(expected))
        self.assertTrue(np.array_equal(game._game_board._game_board, np.array(expected)))

    def test_double(self):
        game = Game()
        game._game_board._game_board = np.array(
            [[0, 0, 0, 0],
            [4, 4, 8, 8],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
        )
        game.do_action("4")
        x, y = game.get_new_pos()
        expected = [
            [0, 0, 0, 0],
            [8, 16, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
        expected[x][y] = 2
        print('\n',game._game_board._game_board, '\n\n', np.array(expected))
        self.assertTrue(np.array_equal(game._game_board._game_board, np.array(expected)))

    def test_up_left(self):
        game = Game()
        game._game_board._game_board = np.array(
            [[2, 0, 0, 0],
            [0, 4, 0, 0],
            [0, 0, 4, 0],
            [0, 0, 0, 8]]
        )
        game.do_action("7")
        x, y = game.get_new_pos()
        expected = [
            [2, 0, 0, 0],
            [0, 8, 0, 0],
            [0, 0, 8, 0],
            [0, 0, 0, 0]]
        expected[x][y] = 2
        print('\n',game._game_board._game_board, '\n\n', np.array(expected))
        self.assertTrue(np.array_equal(game._game_board._game_board, np.array(expected)))

    def test_invalid(self):
        game = Game()
        game._game_board._game_board = np.array(
            [[0, 0, 0, 0],
            [4, 0, 0, 0],
            [4, 0, 0, 0],
            [0, 0, 0, 0]]
        )
        self.assertTrue(not game.valid_action(action="4"))

    def test_lose(self):
        game = Game()
        game._game_board._game_board = np.array(
            [[2, 256, 2, 256],
            [4, 128, 4, 128],
            [8, 64, 8, 64],
            [16, 32, 16, 32]]
        )
        self.assertTrue(game.game_over)


if __name__ == "__main__":    
    test_suite = ut.TestLoader().loadTestsFromTestCase(GameTestCase)
    res = ut.TextTestRunner(verbosity=2).run(test_suite)
    num, errs, fails = res.testsRun, len(res.errors), len(res.failures)
    print("%d of %d passed (%d errors, %d failures)" % (num - (errs+fails), num, errs, fails))