import math
import random
from copy import deepcopy


class Player:
    """
    A player in a Mancala game that has a name and holding representing the
    seeds in the players hand. Has methods for picking up and dropping seeds
    which update the amount stored in _holding, as well as methods to return
    the values stored in its data members.
    """

    def __init__(self, name):
        self._name = name
        self._holding = 0

    def pickup_seeds(self, amount):
        """
        Picks up the amount of seeds and adds to holding.

        :param amount: The number of seeds being picked up.
        """
        self._holding += amount

    def drop_seeds(self, amount):
        """
        Drops the amount of seeds from _holding.

        :param amount: The number of seeds to drop.
        :return: Integer of the number of seeds dropped.
        """
        if amount <= self._holding:
            self._holding -= amount
            return amount

    def drop_all_seeds(self):
        """
        Drops all the seeds in _holding.

        :return: Integer of the number of seeds dropped.
        """
        return self.drop_seeds(self._holding)

    def number_of_seeds_in_hand(self):
        """
        :return: Integer stored in _holding
        """
        return self._holding

    def get_name(self):
        """
        :return: String stored in _name
        """
        return self._name


class Ai(Player):
    def __init__(self, board_obj, name='AI'):
        super().__init__(name)
        self._board_obj = board_obj

    def get_valid_moves(self, side=2, board=None):
        if not board:
            board = self._board_obj
        return board.get_pits_with_seeds(side)


class HardAi(Ai):
    def __init__(self, board_obj):
        super().__init__(board_obj, 'HARD AI')
        self.board_copy = board_obj

    def choose_move(self, MancalaClass):
        moves = self.get_valid_moves()
        depth = 8

        # make fake game to simulate moves on
        game = MancalaClass()
        game.create_player('1')
        game.create_player('2')
        # set fake game state equal to current game state
        # with copy of current board
        state = (2, deepcopy(self._board_obj.get_board()), False,
                 None, False)
        game.restore_state(state)

        ratings = [0] * len(moves)
        for i, move in enumerate(moves):
            saved = game.copy_state()
            game.play_game(2, move)
            cur_eval = self.minimax(game, depth,
                                    float(-math.inf), float(math.inf))
            ratings[i] = cur_eval
            game.restore_state(saved)

        max_idx = [0]
        for i in range(1, len(ratings)):
            if ratings[i] > ratings[max_idx[0]]:
                max_idx = [i]
            if ratings[i] == ratings[max_idx[0]]:
                max_idx.append(i)
        if len(max_idx) > 1:
            # pick a random index if they are equally rated
            return moves[max_idx[random.randint(0, len(max_idx) - 1)]]
        return moves[max_idx[0]]

    def minimax(self, game, depth, alpha, beta):
        if (depth == 0 or game.get_end_state() or
                game.get_board_obj().store_has_seeds_to_win()):
            return self.evaluation(game.get_board())
        turn = game.get_turn()
        moves = self.get_valid_moves(turn, game.get_board_obj())
        if not moves:
            return self.evaluation(game.get_board())
        # maximising
        if turn == 2:
            max_eval = float(-math.inf)
            for move in moves:
                saved = game.copy_state()
                game.play_game(turn, move)
                cur_eval = self.minimax(game, depth - 1, alpha, beta)
                game.restore_state(saved)
                max_eval = max(max_eval, cur_eval)
                alpha = max(alpha, cur_eval)
                if beta <= alpha:
                    break
            return max_eval
        # minimizing
        else:
            min_eval = float(math.inf)
            for move in moves:
                saved = game.copy_state()
                game.play_game(turn, move)
                cur_eval = self.minimax(game, depth - 1, alpha, beta)
                game.restore_state(saved)
                min_eval = min(min_eval, cur_eval)
                beta = min(beta, cur_eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluation(self, board):
        store1 = board[0][6]
        store2 = board[1][6]
        if store2 > 24:
            return 100
        if store1 > 24:
            return -100
        if store1 == 24 and store2 == 24:
            return 0
        return store2 - store1


class EasyAi(Ai):
    def __init__(self, board_obj):
        super().__init__(board_obj, 'EASY AI')

    def choose_move(self):
        moves = self.get_valid_moves()
        idx = random.randint(0, len(moves) - 1)
        return moves[idx]
