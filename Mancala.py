from copy import deepcopy

from Board import Board
from Player import Player, EasyAi, HardAi


class Mancala:
    """
    Mancala class representing a Mancala game which controls the state of the
    game, and has methods to complete a turn, and check for special conditions
    and winning conditions.
    """

    def __init__(self, gui=None):
        self._turn = 1
        self._players = []
        self._board = Board(gui)
        self._gui = gui
        self._ended = False
        self._winner = None
        self.special1 = False

    def get_board(self):
        return self._board.get_board()

    def get_board_obj(self):
        return self._board

    def get_turn(self):
        return self._turn

    def reset(self, reset_players=False):
        self._turn = 1
        self._board.reset()
        self._ended = False
        self._winner = None
        self.special1 = False
        if reset_players:
            self._players = []

    def copy_state(self):
        return (self._turn, deepcopy(self._board.get_board()), self._ended,
                self._winner, self.special1)

    def restore_state(self, saved_state):
        (self._turn, board, self._ended,
         self._winner, self.special1) = saved_state
        self._board.set_board(board)

    def create_player(self, name):
        """
        Creates a new player object and stores it in _players data member.
        Only creates a player if there are less than 2.

        :param name: String of the players name.

        :return: Player object that was created.
        """
        if len(self._players) < 2:
            player_num = len(self._players) + 1
            if name == -1:
                player = EasyAi(self._board, player_num)
            elif name == -2:
                player = HardAi(self._board, player_num)
            else:
                player = Player(name, player_num)
            self._players.append(player)
            return player

    def get_end_state(self):
        """
        Returns boolean if game has already ended

        :return: Boolean self._ended
        """
        return self._ended

    def play_game(self, player, pit):
        """
        Plays an entire turn, first validates the input and state of the game,
        and makes the move in the pit by calling make_move. Then checks if the
        game is over, updating board, _ended, and _winner, and finally
        returns a list of the updated board.

        :param player: The player number (1 or 2).
        :param pit: The pit number (1-6).

        :return:
            If player or pit number is invalid returns a string.
            If game is ended returns "Game is ended" string.
            Otherwise, returns a list showing the current state of the board.
        """
        # only plays the game if there are 2 players
        if len(self._players) == 2:
            if self._ended:
                return "Game is ended"
            # validate the inputs
            if not 1 <= player <= 2:
                return "Invalid player number"
            if not 1 <= pit <= 6:
                return "Invalid number for pit index"
            if player != self._turn:
                return "Not Your Turn"

            # only makes the move if there are seeds in the pit
            if self._board.get_seeds_in_pit(self._turn, pit):
                self.make_move(pit)
                if self.is_end():
                    self.end_game()
                else:
                    if not self.special1:
                        self.toggle_turn()
                    else:
                        self.special1 = False
            return self._board.flat()

    def make_move(self, pit):
        """
        The current player picks up the seeds in the pit, then calls
        drop_seeds_in_pits to drop the seeds in each pit and checks for special
        rules after dropping the last seed.

        :param pit: The pit number (1-6).
        """
        self.get_player_obj().pickup_seeds(
            self._board.clear_pit(self._turn, pit))
        self.drop_seeds_in_pits(pit)

    def drop_seeds_in_pits(self, start_pit):
        """
        Drops a seed that the current player is holding in the next pit on the
        board until the player runs out of seeds. Then calls check_special.

        :param start_pit: The starting pit number (1-6)
        """
        player = self.get_player_obj()
        side, pit = self._turn, start_pit
        while player.number_of_seeds_in_hand() > 0:
            side, pit = self._board.get_next_pit(self._turn, side, pit)
            player.drop_seeds(1)
            self._board.add_seeds(side, pit, 1)
        self.check_special(side, pit)

    def is_end(self):
        """:return: Boolean if there are seeds in the current player's pits"""
        return not self._board.has_seeds_on_side(self._turn)

    def end_game(self):
        """
        Opponent takes all the seeds on their side and adds to their store.
        Sets data members for ended, and winner.
        """
        self.toggle_turn()

        # all seeds on opponents side goes to store
        self.pickup_all_on_side()
        player = self.get_player_obj()
        self._board.add_seeds(self._turn, 7, player.drop_all_seeds())

        # sets data members for ended and winner
        self._ended = True
        self._winner = self.get_winner()

    def get_player_obj(self):
        """:return: Player object for the current player based on the turn."""
        return self._players[self._turn - 1]

    def toggle_turn(self):
        """
        Changes turn from 1 to 2 or 2 to 1.
        """
        if self._turn == 1:
            self._turn = 2
        else:
            self._turn = 1

    def pickup_all_on_side(self):
        """
        Current player picks up all the seeds from the pits on their side of
        the board.
        """
        player = self.get_player_obj()

        for i in range(1, 7):
            player.pickup_seeds(self._board.clear_pit(self._turn, i))

    def check_special(self, last_side, last_pit):
        """
        Checks for special rules 1 and 2 by first checking if the last seed was
        placed on the current player's side, returning if not true.
        Then checks if the last seed was placed in the store, printing a string
        if true. Otherwise, checks if the last seed was placed in an empty
        pit, capturing the opposing and last placed seeds if true.

        :param last_side: The side of the board of the last seed (1 or 2).
        :param last_pit: The pit number that last seed was placed on (1-7).
        """
        if last_side != self._turn:
            return
        # check special rule 1, last seed placed in player's store (pit 7)
        # but if the game is over skip
        if last_pit == 7:
            if self._board.has_seeds_on_side(self._turn):
                self.special1 = True
                # print(f'player {self._turn} take another turn')

        # check special rule 2, last seed placed in empty pit (pit has 1 seed)
        elif self._board.get_seeds_in_pit(last_side, last_pit) == 1:
            # take opposite seeds
            player = self.get_player_obj()
            opp_seeds = self._board.clear_opposite(last_side, last_pit)
            # if there are no seeds on the opposite side do nothing
            if not opp_seeds:
                return
            player.pickup_seeds(opp_seeds)
            # take last seed placed
            player.pickup_seeds(self._board.clear_pit(last_side, last_pit))
            # put in store (pit 7 on player's side equal to turn)
            self._board.add_seeds(self._turn, 7, player.drop_all_seeds())

    def get_winner(self):
        """
        If the game is ended compares the scores and returns the result.

        :return: If the game is not ended None, otherwise integer of the
            winning player number or the string "tie".
        """
        if self._ended:
            player1_score = self._board.get_seeds_in_store(1)
            player2_score = self._board.get_seeds_in_store(2)
            if player1_score == player2_score:
                return "tie"
            if player1_score > player2_score:
                return 1
            else:
                return 2

    def return_winner(self):
        """
        Returns a string representing the winner or state of the game.

        :return: String for the winning player, a tie, or if game is not ended.
        """
        if not self._ended or not self._winner:
            return "Game has not ended"
        if self._winner == 'tie':
            return "It's a tie"
        if self._winner == 1:
            return f'Winner is player 1: {self._players[0].get_name()}'
        return f'Winner is player 2: {self._players[1].get_name()}'

    def take_opposite_seeds(self, side, pit):
        """
        The player picks up the seeds on the opposite side of the board and
        places them in their store.

        :param side: The side of the board (1 or 2).
        :param pit: The pit to take the opposite sides seeds from (1-6).
        """
        player = self.get_player_obj()
        # pickup seeds on opposite side
        player.pickup_seeds(self._board.clear_opposite(side, pit))
        # add seeds picked up to store (pit 7 on player's side equal to turn)
        self._board.add_seeds(self._turn, 7, player.drop_all_seeds())

    def print_board(self):
        """
        Prints for each player, the number of seeds in the store, and a list
        showing the number of seeds in each pit from pits 1 to 6.
        """
        to_print = f'player1:\nstore: {self._board.get_seeds_in_store(1)}\n' \
                   f'{self._board.get_players_pits(1)}\n' \
                   f'player2:\nstore: {self._board.get_seeds_in_store(2)}\n' \
                   f'{self._board.get_players_pits(2)}'
        print(to_print)

    def get_stores(self):
        """
        Returns the number of seeds in player 1 and player 2 stores

        :return: Tuple for  integer of player1 store, integer of player2 store
        """
        return (self._board.get_seeds_in_store(1),
                self._board.get_seeds_in_store(2))

    def get_player_names(self):
        if len(self._players) == 2:
            return self._players[0].get_name(), self._players[1].get_name()
