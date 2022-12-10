import random


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

    def get_valid_moves(self):
        return self._board_obj.get_pits_with_seeds(2)


class HardAi(Ai):
    def __init__(self, board_obj):
        super().__init__(board_obj, 'HARD AI')


class EasyAi(Ai):
    def __init__(self,board_obj):
        super().__init__(board_obj, 'EASY AI')

    def choose_move(self):
        moves = self.get_valid_moves()
        idx = random.randint(0, len(moves) - 1)
        return moves[idx]