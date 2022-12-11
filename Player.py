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

    def get_valid_moves(self, side=2):
        return self._board_obj.get_pits_with_seeds(side)


class HardAi(Ai):
    def __init__(self, board_obj):
        super().__init__(board_obj, 'HARD AI')
        self.board_copy = board_obj

    def choose_move(self, MancalaClass):
        print('hard ai choose')
        print('board', self._board_obj.get_board())

        original_board_state = deepcopy(self._board_obj.get_board())

        moves = self.get_valid_moves()
        print('moves ', moves)
        # make fake game to simulate moves on
        game = MancalaClass()
        game.create_player('1')
        game.create_player('2')
        game.toggle_turn()

        game._board.set_board(self._board_obj.get_board())
        self._board_obj = game._board

        ratings = [0] * len(moves)
        for i, move in enumerate(moves):
            print('trying move: 2, ', move)
            game.play_game(2, move)
            rating = self.get_move_rating(game)
            ratings[i] = rating
            game.reset()
            game.toggle_turn()
            game._board.set_board(deepcopy(original_board_state))

        # restore board_obj
        self._board_obj = self.board_copy
        self._board_obj.set_board(original_board_state)

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

    def get_move_rating(self, game, depth=1):
        moves = self.get_valid_moves(game.get_turn())
        store1 = self._board_obj.get_seeds_in_store(1)
        store2 = self._board_obj.get_seeds_in_store(2)
        if (depth > 6 or not moves or store1 > 24 or store2 > 24 or
                (store1 == 24 and store2 == 24)):
            if self._board_obj.get_seeds_in_store(2) > 24:
                return 100
            if store1 == 24 and store2 == 24:
                return 0
            return store2 - store1
        copy_board_state = deepcopy(self._board_obj.get_board())
        turn = game.get_turn()
        total = 0
        for move in moves:
            game.play_game(turn, move)
            game.reset()
            if turn == 2:
                game.toggle_turn()
            game._board.set_board(deepcopy(copy_board_state))
            if (turn == 2 and self._board_obj.get_seeds_in_store(2) <= store2):
                continue
            total += self.get_move_rating(game, depth+1)
        return total


class EasyAi(Ai):
    def __init__(self, board_obj):
        super().__init__(board_obj, 'EASY AI')

    def choose_move(self):
        moves = self.get_valid_moves()
        idx = random.randint(0, len(moves) - 1)
        return moves[idx]
