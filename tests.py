from Mancala import Mancala, Board, Player
import unittest
from unittest.mock import patch


class MancalaTest(unittest.TestCase):
    def test1(self):
        """create_player"""
        # adding a player adds player to _players list
        m = Mancala()
        lisa = m.create_player('Lisa')
        self.assertTrue(len(m._players) == 1)
        m.create_player('Fink')
        self.assertTrue(len(m._players) == 2)
        # can only add two players
        m.create_player('Imposter')
        self.assertTrue(len(m._players) == 2)
        # added in correct order
        self.assertEqual(m._players[0].get_name(), 'Lisa')
        self.assertEqual(m._players[1].get_name(), 'Fink')
        # returns player
        self.assertTrue(isinstance(lisa, Player))

    def test2(self):
        """get_player_obj"""
        game = Mancala()
        p1 = game.create_player("Lisa")
        self.assertEqual(game.get_player_obj().get_name(), "Lisa")
        p2 = game.create_player("Fink")
        game._turn = 2  # manually change turn
        self.assertEqual(game.get_player_obj().get_name(), "Fink")

    def test3(self):
        """is_end"""
        game = Mancala()
        self.assertFalse(game.is_end())
        # manually adjust board to trigger end
        game._board._board[0] = [0, 0, 0, 0, 0, 0, 0]
        self.assertTrue(game.is_end())
        # manually adjust turn to make sure it is checking the correct side
        game._turn = 2
        self.assertFalse(game.is_end())

    def test4(self):
        """toggle_turn"""
        game = Mancala()
        game.toggle_turn()
        self.assertEqual(game._turn, 2)
        game.toggle_turn()
        self.assertEqual(game._turn, 1)

    def test5(self):
        """pickup_all_on_side"""
        game = Mancala()
        game.create_player('name')
        game.create_player('name')
        game.pickup_all_on_side()
        board_should_be = [0,0,0,0,0,0,0]
        self.assertListEqual(game._board._board[0], board_should_be)
        # player1 has the seeds
        self.assertEqual(game.get_player_obj().number_of_seeds_in_hand(), 24)
        # test that it picks up on player 2 side if turn is 2
        game.toggle_turn()
        game.pickup_all_on_side()
        self.assertListEqual(game._board._board[1], board_should_be)
        # player2 has the seeds
        self.assertEqual(game.get_player_obj().number_of_seeds_in_hand(), 24)

    def test6(self):
        """get_winner"""
        game = Mancala()
        game.create_player('name')
        game.create_player('name')
        # no winner if game isn't ended
        self.assertEqual(game.get_winner(), None)
        game._ended = True
        self.assertEqual(game.get_winner(), "tie")
        # add seeds to player2 store and test with player2 winner
        game._board.add_seeds(2, 7, 10)
        self.assertEqual(game.get_winner(), 2)
        # add seeds to player1 store and test with player1 winner
        game._board.add_seeds(1, 7, 100)
        self.assertEqual(game.get_winner(), 1)

    def test7(self):
        """return_winner"""
        game = Mancala()
        game.create_player('Lisa')
        game.create_player('Fink')
        winner = game.return_winner()
        p1_win = "Winner is player 1: Lisa"
        p2_win = "Winner is player 2: Fink"
        tie = "It's a tie"
        not_ended = "Game has not ended"
        self.assertEqual(game.return_winner(), not_ended)

        game._ended = True
        # tie game
        game._winner = game.get_winner()
        self.assertEqual(game.return_winner(), tie)

        # player1 wins
        game._board.add_seeds(1,7,50)
        game._winner = game.get_winner()
        self.assertEqual(game.return_winner(), p1_win)

        # player2 wins
        game._board.add_seeds(2,7,150)
        game._winner = game.get_winner()
        self.assertEqual(game.return_winner(), p2_win)

    def test8(self):
        """take_opposite_seeds"""
        game = Mancala()
        game.create_player('Lisa')
        game.create_player('Fink')
        game.take_opposite_seeds(1, 5)
        board_should_be = [[4,4,4,4,4,4,4], [4,0,4,4,4,4,0]]
        self.assertListEqual(board_should_be, game._board._board)

    @patch('builtins.print')
    def test9(self, mock_print):
        """print_board"""
        game = Mancala()
        game.create_player('Lisa')
        game.create_player('Fink')
        game.print_board()
        mock_print.assert_called_with(
            'player1:\nstore: 0\n[4, 4, 4, 4, 4, 4]\nplayer2:\nstore: 0\n[4, 4, 4, 4, 4, 4]')

        # manually change score and check if it still works
        game._board._board = [[0,0,0,0,0,0,30],[6,6,6,5,4,3,10]]
        game.print_board()
        mock_print.assert_called_with(
        'player1:\nstore: 30\n[0, 0, 0, 0, 0, 0]\nplayer2:\nstore: 10\n[6, 6, 6, 5, 4, 3]')

    @patch('builtins.print')
    def test10(self, mock_print):
        """check_special"""
        # nothing changes or outputs if last pit is on opponent side
        game = Mancala()
        game.create_player('name')
        game.create_player('name')
        board_should_be = list(game._board._board)
        game.check_special(2,1)
        self.assertListEqual(game._board._board, board_should_be)
        mock_print.assert_not_called()

        # special rule 2 no print
        game._board._board[0][3] = 1  # manually set board
        game.check_special(1, 4)
        mock_print.assert_not_called()

        # reset board
        game._board._board = board_should_be

        # special rule 1 for player 1
        game.check_special(1, 7)
        mock_print.assert_called_with("player 1 take another turn")

        # special rule 1 for player 2
        game.toggle_turn()
        game.check_special(2, 7)
        mock_print.assert_called_with("player 2 take another turn")

        # special rule 2 for player 1
        game = Mancala()
        game.create_player('name')
        game.create_player('name')
        game._board._board[0][3] = 1  # manually set board
        game.check_special(1, 4)
        board_should_be = [[4,4,4,0,4,4,5], [4,4,0,4,4,4,0]]
        self.assertListEqual(game._board._board, board_should_be)

        # special rule 2 for player 2
        game._board._board[1][5] = 1  # manually set board
        game.toggle_turn()
        game.check_special(2, 6)
        board_should_be = [[0,4,4,0,4,4,5], [4,4,0,4,4,0,5]]
        self.assertListEqual(game._board._board, board_should_be)

    @patch('builtins.print')
    def test11(self, mock_print):
        """drop_seeds_in_pits"""
        game = Mancala()
        p1 = game.create_player("Lisa")
        p2 = game.create_player("Fink")
        # pickup 4 from side
        start_pit = 1
        game.get_player_obj().pickup_seeds(game._board.clear_pit(1, 1))
        game.drop_seeds_in_pits(start_pit)
        changed_board = game._board._board[0]
        board_should_be = [0, 5, 5, 5, 5, 4, 0]
        self.assertListEqual(changed_board, board_should_be)
        mock_print.assert_not_called()  # special 1 doesn't get triggered

        # correctly calls check_special & triggers special rule 2
        game = Mancala()
        p1 = game.create_player("Lisa")
        p2 = game.create_player("Fink")
        game._board._board = [[0,0,0,0,0,0,0],[0,0,10,0,0,0,0]]
        player = game.get_player_obj()
        player.pickup_seeds(3)
        game.drop_seeds_in_pits(1)
        board_should_be = [[0,1,1,0,0,0,11], [0,0,0,0,0,0,0]]
        self.assertListEqual(game._board._board, board_should_be)

        # correctly calls check_special & triggers special rule 1
        game = Mancala()
        p1 = game.create_player("Lisa")
        p2 = game.create_player("Fink")
        player = game.get_player_obj()
        player.pickup_seeds(3)
        game.drop_seeds_in_pits(4)
        mock_print.assert_called_with("player 1 take another turn")

        # correctly calls check_special & triggers special rule 1 player2
        game.toggle_turn()
        player = game.get_player_obj()
        player.pickup_seeds(3)
        game.drop_seeds_in_pits(4)
        mock_print.assert_called_with("player 2 take another turn")

    def test12(self):
        """make_move"""
        game = Mancala()
        game.create_player('name')
        game.create_player('name')
        game.make_move(1)
        board_should_be = [[0,5,5,5,5,4,0],[4,4,4,4,4,4,0]]
        self.assertListEqual(game._board._board, board_should_be)

    def test13(self):
        """end_game"""
        game = Mancala()
        game.create_player('name')
        game.create_player('name')
        # end_game moves opponent's seeds to opponent's store
        game._board._board = [[0,0,0,0,0,0,0], [10,10,10,10,10,10,0]]
        game.end_game()
        board_should_be = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,60]]
        self.assertListEqual(game._board._board, board_should_be)
        # end_game sets _ended and _winner
        self.assertTrue(game._ended)
        self.assertTrue(game._winner is not None)

    def test14(self):
        """play_game"""
        game = Mancala()
        game.create_player('name')

        # # need 2 players
        # self.assertEqual("Need 2 players to play game!", game.play_game(1,6))

        game.create_player('name')
        # invalid player number
        self.assertEqual("Invalid player number", game.play_game(0, 6))
        self.assertEqual("Invalid player number", game.play_game(3, 6))
        # invalid pit
        self.assertEqual("Invalid number for pit index", game.play_game(1, 0))
        self.assertEqual("Invalid number for pit index", game.play_game(1, 7))
        # game is ended
        game._ended = True
        self.assertEqual("Game is ended", game.play_game(1,1))

        game._ended = False

        # calls make move correctly
        game.play_game(1,1)
        board_should_be = [[0,5,5,5,5,4,0], [4,4,4,4,4,4,0]]
        self.assertEqual(game._board._board, board_should_be)

        # calls is_end
        game._board._board = [[0,0,0,0,0,1,0],[0,0,0,0,0,0,0]]
        game.play_game(1,6)
        self.assertTrue(game._ended)

        # returns the flat board
        # reset board
        game = Mancala()
        game.create_player('name')
        game.create_player('name')
        should_be = [4, 4, 0, 5, 5, 5, 1, 4, 4, 4, 4, 4, 4, 0]
        self.assertListEqual(should_be, game.play_game(1, 3))


class BoardTest(unittest.TestCase):
    def test1(self):
        """test flat"""
        board = Board()
        flat = board.flat()
        res = [4,4,4,4,4,4,0, 4,4,4,4,4,4,0]
        self.assertListEqual(flat, res)

    def test2(self):
        """test clear_pit"""
        board = Board()

        seeds_returned = board.clear_pit(1,1)
        # clear pit returns correct number
        self.assertEqual(seeds_returned, 4)
        # clear pit clears the index
        self.assertEqual(board._board[0][0], 0)

    def test3(self):
        """test get_opposite_pit"""
        board = Board()
        opp = board.get_opposite_pit(1,3)
        self.assertEqual(opp, (2,4))
        opp = board.get_opposite_pit(2, 1)
        self.assertEqual(opp, (1,6))

    def test4(self):
        """get_seeds_in_pit"""
        b = Board()
        b._board[0][0] = 17  # manually adjusts board
        self.assertEqual(b.get_seeds_in_pit(1, 1), 17)
        self.assertEqual(b.get_seeds_in_pit(1, 5), 4)

    def test5(self):
        """clear opposite"""
        board = Board()
        cleared = board.clear_opposite(1, 2)
        self.assertEqual(cleared, 4)
        self.assertEqual(board.get_seeds_in_pit(2, 5), 0)

        # try different index to clear
        cleared = board.clear_opposite(2, 1)
        self.assertEqual(cleared, 4)
        self.assertEqual(board.get_seeds_in_pit(1, 6), 0)

    def test6(self):
        """get_next_pit"""
        board = Board()
        side, pit = 1, 1
        turn = 1
        # traverse pit to pit
        res = board.get_next_pit(turn, side, pit)
        next_pit = (1, 2)
        self.assertEqual(res, next_pit)
        # traverse into player's store
        side, pit = (1, 6)
        turn = 1
        res = board.get_next_pit(turn, side, pit)
        next_pit = (1, 7)
        self.assertEqual(res, next_pit)
        # skip over opponent's store
        side, pit = (2, 6)
        turn = 1
        res = board.get_next_pit(turn, side, pit)
        next_pit = (1, 1)
        self.assertEqual(res, next_pit)

    def test7(self):
        """get_seeds_in_store"""
        b = Board()
        amt = b.get_seeds_in_store(1)
        self.assertEqual(amt, 0)

    def test8(self):
        """has_seeds_on_side"""
        b = Board()
        self.assertTrue(b.has_seeds_on_side(1))
        b._board[0] = [0,0,0,0,0,0,0]
        self.assertFalse(b.has_seeds_on_side(1))

    def test9(self):
        """add_seeds"""
        b = Board()
        b.add_seeds(1, 1, 20)
        pit_added = b.get_seeds_in_pit(1, 1)
        self.assertEqual(pit_added, 24)

    def test10(self):
        """get_players_pits"""
        b = Board()
        ans = [4, 4, 4, 4, 4, 4]
        res = b.get_players_pits(1)
        self.assertListEqual(ans, res)
        b.clear_pit(1, 1)
        ans = [0, 4, 4, 4, 4, 4]
        res = b.get_players_pits(1)
        self.assertListEqual(ans, res)

    def test_get_pits_with_seeds_new_board(self):
        b = Board()
        res = b.get_pits_with_seeds(1)
        self.assertListEqual([1,2,3,4,5,6], res)

    def test_get_pits_with_seeds_pit_4_empty(self):
        b = Board()
        b._board[0] = [4, 4, 4, 0, 4, 4, 0]
        res = b.get_pits_with_seeds(1)
        self.assertListEqual([1,2,3,5,6], res)

    def test_get_pits_with_seeds_1_pit_not_empty(self):
        b = Board()
        b._board[0] = [4,0,0,0,0,0,0]
        res = b.get_pits_with_seeds(1)
        self.assertListEqual([1], res)

    def test_get_pits_with_seeds_side_2(self):
        b = Board()
        res = b.get_pits_with_seeds(2)
        self.assertListEqual([1, 2, 3, 4, 5, 6], res)

    def test_get_pits_with_seeds_in_store(self):
        b = Board()
        b._board[0] = [4, 4, 4, 4, 4, 4, 4]
        res = b.get_pits_with_seeds(1)
        self.assertListEqual([1,2,3,4,5,6], res)


class PlayerTests(unittest.TestCase):
    def test1(self):
        """number_of_seeds_in_hand"""
        p = Player('name')
        res = p.number_of_seeds_in_hand()
        self.assertEqual(res, 0)
        p._holding = 100  # manual change
        res = p.number_of_seeds_in_hand()
        self.assertEqual(res, 100)

    def test2(self):
        """pickup_seeds"""
        p = Player('name')
        p.pickup_seeds(1)
        self.assertEqual(p.number_of_seeds_in_hand(), 1)
        p.pickup_seeds(24)
        self.assertEqual(p.number_of_seeds_in_hand(), 25)

    def test3(self):
        """drop_seeds"""
        p = Player('name')
        p.pickup_seeds(25)
        self.assertEqual(p.drop_seeds(1), 1)
        self.assertEqual(p.drop_seeds(10), 10)
        self.assertEqual(p.number_of_seeds_in_hand(), 14)

    def test4(self):
        """drop_all_seeds"""
        p = Player('name')
        p.pickup_seeds(25)
        self.assertEqual(p.drop_all_seeds(), 25)
        self.assertEqual(p.number_of_seeds_in_hand(), 0)

    def test5(self):
        """get_name"""
        p = Player('Lisa')
        self.assertEqual(p.get_name(), 'Lisa')

    def test6(self):
        """Easy ai initialized with name"""
        game = Mancala()
        game.create_player('Lisa')
        ai = game.create_player(-1)
        self.assertEqual(ai.get_name(), 'EASY AI')

    def test_choose_move_in_correct_range(self):
        """Easy ai choose_move with full board"""
        game = Mancala()
        game.create_player('Lisa')
        ai = game.create_player(-1)
        move = ai.choose_move()

        # tests res in range
        for i in range(20):
            self.assertLessEqual(move, 6)
            self.assertGreaterEqual(move, 1)

    @patch('random.randint')
    def test_choose_move_as_generated(self, random_call):
        game = Mancala()
        game.create_player('Lisa')
        ai = game.create_player(-1)

        random_call.return_value = 4
        for i in range(20):
            move = ai.choose_move()
            self.assertEqual(random_call.return_value + 1, move)

    def test_choose_move_board_has_1_move(self):
        game = Mancala()
        game.create_player('Lisa')
        ai = game.create_player(-1)
        game._board._board[1] = [0,0,0,0,0,1,0]
        move = ai.choose_move()
        self.assertEqual(6, move)






