class Board:
    """
    A board for a Mancala game that has a board data member, a 2d list,
    representing the pits and stores on a Mancala board with values
    representing the seeds that go in the pits and stores.
    Has methods for updating the seeds in the pits and stores, getting the
    amount of seeds in particular pits or stores, traveling around the board
    following the rules of the game, and representing the board as different
    formatted lists.
    """

    def __init__(self, gui=None):
        self._board = [[4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0]]
        if gui:
            self._show_changes = True
        else:
            self._show_changes = False
        self._gui = gui

    def set_show_changes(self, show_bool):
        """
        Sets _show_changes.

        :param: show_bool: Boolean to set _show_changes.
        """
        self._show_changes = show_bool

    def get_board(self):
        """
        :return: List for the _board, 7x7 list of integers.
        """
        return self._board

    def set_board(self, board):
        """
        Sets _board to a new list.

        :paran: board: 7x7 List of integers.
        """
        self._board = board

    def update_gui(self, side, pit, amount):
        """
        Adjusts side and pit in gui to have +/- amount seeds.

        :param side: The side of the board (1 or 2).
        :param pit: The pit to be cleared (1-6).
        :param amount: Positive or negative integer of amount of seeds changed.
        """
        self._gui.update_pit(side, pit, amount)

    def reset(self):
        self._board = [[4, 4, 4, 4, 4, 4, 0], [4, 4, 4, 4, 4, 4, 0]]
        if self._gui:
            self._show_changes = True

    def get_pits_with_seeds(self, side):
        """
        Returns a list of the pit numbers on side with values > 0

        :param side: The side of the board (1 or 2).
        """
        res = []
        for i in range(len(self._board[side - 1]) - 1):
            if self._board[side - 1][i] > 0:
                res.append(i + 1)
        return res

    def flat(self):
        """
        Returns a flattened copy of the 2d board stored in board using list
        comprehension.

        :return: List of the seeds in each pit and store.
        """
        return [pit for side in self._board for pit in side]

    def clear_pit(self, side, pit):
        """
        Takes all the seeds out of the pit, and returns the number of seeds
        that were cleared.

        :param side: The side of the board (1 or 2).
        :param pit: The pit to be cleared (1-6).
        :return: Integer of the number of seeds that were cleared from the pit.
        """
        seeds = self._board[side - 1][pit - 1]
        self._board[side - 1][pit - 1] = 0
        if self._show_changes and seeds > 0:
            self.update_gui(side, pit, -seeds)
        return seeds

    def clear_opposite(self, side, pit):
        """
        Finds the opposite pit, clears the opposite pit, and returns the number
        of seeds that were cleared.

        :param side: The current player's number (1 or 2).
        :param pit: The pit to clear the opposite of (nums 1-6).
        :return: Integer of the number of seeds cleared from the opposite pit.
        """
        opposite_turn, opposite_pit = self.get_opposite_pit(side, pit)
        return self.clear_pit(opposite_turn, opposite_pit)

    def get_opposite_pit(self, side, pit):
        """
        Finds the opposite side and pit number.

        :param side: The side of the board (1 or 2).
        :param pit: The pit number (1-6).
        :return: Tuple of the opposite side number, and opposite pit number.
        """
        # get opposite side
        opposite_side = 1
        if side == 1:
            opposite_side = 2
        # get opposite of pit number
        opposite_pit = 7 - pit
        return opposite_side, opposite_pit

    def get_next_pit(self, turn, side, pit):
        """
        Returns the next pit that a seed can be placed in by going
        counterclockwise skipping the opponents store.

        :param turn: The current player number (1 or 2).
        :param side: The side of the board (1 or 2).
        :param pit: The pit number (1-7).
        :return: Tuple containing the side and pit of the next pit.
        """
        # check if changing sides of board
        # player's store (pit 7) or opponents last pit (pit 6)
        if (side == turn and pit == 7) or (side != turn and pit == 6):
            pit = 1
            # toggles side
            if side == 1:
                side = 2
            else:
                side = 1
        else:
            pit += 1
        return side, pit

    def get_seeds_in_store(self, player_num):
        """
        Returns the seeds in the player's store.

        :param player_num: The player number (1 or 2).
        :return: Integer of the number of seeds in the player's store.
        """
        return self._board[player_num - 1][6]

    def store_has_seeds_to_win(self):
        """
        :return: Boolean for if one of the stores has over 24 seeds.
        """
        return self._board[0][6] > 24 or self._board[1][6] > 24

    def has_seeds_on_side(self, side):
        """
        Iterates through the pits on the side returning a boolean for if there
        is a seed.

        :param side: The side of the board (1 or 2).
        :return: Boolean for if there are any seeds in the pits on the side.
        """
        side_of_board = self._board[side - 1]
        for i in range(6):  # loops for 6 pits
            if side_of_board[i] > 0:
                return True
        return False

    def add_seeds(self, side, pit, amount):
        """
        Adds amount to the total seeds in the pit.

        :param side: The side of the board (1 or 2).
        :param pit: The pit number (1-7).
        :param amount: The amount of seeds to add.
        """
        self._board[side - 1][pit - 1] += amount
        if self._show_changes:
            self.update_gui(side, pit, amount)

    def get_players_pits(self, player_number):
        """
        Returns a list of the player's pits, the first 6 indices of board, by
        slicing the list.
        :param player_number: The player number (1 or 2).
        :return: List of the six pits on the players side of the board.
        """
        return self._board[player_number - 1][:6]

    def get_seeds_in_pit(self, side, pit):
        """
        Returns the number of seeds in the pit.

        :param side: The side of the board (1 or 2).
        :param pit: The pit number (1-7).
        :return: Integer of the value in board at the side and pit.
        """
        return self._board[side - 1][pit - 1]
