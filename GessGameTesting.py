import unittest
from GessGame import GessGame, Board


class TestGessGame(unittest.TestCase):

    def test_resign_black(self):
        """tests if black resigns, white wins"""
        game = GessGame()
        game.resign_game()
        result = game.get_game_state()
        self.assertEqual(result, "WHITE_WON")

    def test_resign_white(self):
        """tests if white resigns, black wins"""
        game = GessGame()
        game.make_move('c2', 'c3')
        game.resign_game()
        result = game.get_game_state()
        self.assertEqual(result, "BLACK_WON")

    def test_n_no_token(self):
        game = GessGame()
        result = game.make_move('b5', 'b6')
        self.assertEqual(result, False)

    def test_e_no_token(self):
        game = GessGame()
        result = game.make_move('b5', 'c5')
        self.assertEqual(result, False)

    def test_s_no_token(self):
        game = GessGame()
        result = game.make_move('b5', 'b4')
        self.assertEqual(result, False)

    def test_sw_no_token(self):
        game = GessGame()
        result = game.make_move('c5', 'b4')
        self.assertEqual(result, False)

    def test_se_no_token(self):
        game = GessGame()
        result = game.make_move('c6', 'd5')
        self.assertEqual(result, False)

    def test_white_won(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        game.make_move('l18', 'l15')
        game.make_move('c3', 'c4')
        game.make_move('l15', 'l12')
        game.make_move('c4', 'c5')
        game.make_move('l12', 'l9')
        game.make_move('c6', 'c7')
        game.make_move('l9', 'l8')
        game.make_move('c7', 'c8')
        game.make_move('l8', 'l5')
        result = game.get_game_state()
        self.assertEqual(result, "WHITE_WON")

    def test_to_oob_side_black(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        game.make_move('l18', 'l15')
        result = game.make_move('c3', 'a3')
        self.assertEqual(result, False)

    def test_to_oob_top_black(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        game.make_move('l18', 'l15')
        result = game.make_move('c3', 'c1')
        self.assertEqual(result, False)

    def test_black_won(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        game.make_move('l18', 'l15')
        game.make_move('c3', 'c4')
        game.make_move('l15', 'l12')
        game.make_move('c4', 'c5')
        game.make_move('l12', 'l9')
        game.make_move('c6', 'c7')
        game.make_move('l9', 'l8')
        game.make_move('l3', 'l6')
        result = game.get_game_state()
        self.assertEqual(result, "BLACK_WON")

    def test_black_suicide(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        game.make_move('l18', 'l15')
        result = game.make_move('m3', 'm4')
        self.assertEqual(result, False)

    def test_white_suicide(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('m18', 'm16')
        self.assertEqual(result, False)

    def test_north_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('l13', 'l15')
        self.assertEqual(result, True)

    def test_east_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('h14', 'i14')
        self.assertEqual(result, True)

    def test_south_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('i15', 'i16')
        self.assertEqual(result, False)

    def test_west_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('j14', 'h14')
        self.assertEqual(result, True)

    def test_nw_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('k13', 'm15')
        self.assertEqual(result, True)

    def test_ne_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('j13', 'h15')
        self.assertEqual(result, True)

    def test_se_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('h15', 'j13')
        self.assertEqual(result, True)

    def test_sw_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('s15', 'p12')
        self.assertEqual(result, True)

    def test_north_w_false(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('l15', 'l16')
        self.assertEqual(result, False)

    def test_east_w_false(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('h14', 'j16')
        self.assertEqual(result, False)

    def test_south_w_false(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('h15', 'h1')
        self.assertEqual(result, False)

    def test_west_w_false(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('j14', 'j15')
        self.assertEqual(result, False)

    def test_nw_w_false(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('k13', 'j15')
        self.assertEqual(result, False)

    def test_ne_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('j13', 'h13')
        self.assertEqual(result, False)

    def test_se_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('h15', 'g13')
        self.assertEqual(result, False)

    def test_sw_w_true(self):
        game = GessGame()
        game.make_move('c2', 'c3')
        result = game.make_move('n13', 'm13')
        self.assertEqual(result, False)
