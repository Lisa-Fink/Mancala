import pygame
from pygame.locals import *
import pygame.freetype

from Gui import GraphicInterface
from Mancala import Mancala


def check_display_time(gui):
    """Check the display time for pits and remove the changes if necessary.

    Args:
        gui: The GraphicInterface instance.

    This function iterates over the pits that have changes in their display time
    and removes the changes if the elapsed time since the change exceeds 1000 milliseconds.
    It also updates the display to reflect the changes made.
    """
    cur_time = pygame.time.get_ticks()
    for pit in gui.get_pits_changed():
        if pit.time_showing_changed < cur_time - 1000:
            gui.remove_change_display(pit)
            pygame.display.flip()


def main():
    """Main entry point of the Mancala game."""
    gui = GraphicInterface()
    game = Mancala(gui.get_game_gui())
    mode = None

    while True:
        # check if on game screen
        if gui.get_screen_index() == 2:

            if gui.game_gui_showing_changed():
                # removes update if passed time limit
                check_display_time(gui.get_game_gui())

            # check if it is an Ai's turn (set up for Ai always as player 2)
            elif game.get_turn() == 2 and mode != 'TWO':
                arg = None
                if mode == 'HARD':
                    arg = Mancala
                move = game.get_player_obj().choose_move(arg) if arg else \
                    game.get_player_obj().choose_move()
                game.play_game(
                    2, move)
                # check if game ended
                ended = game.get_end_state()

                # updates gui to new turn after move completed
                if not ended:
                    gui.get_game_gui().display_turn(
                        game.get_player_obj().get_name(), game.get_turn())
                else:
                    # go to end game screen
                    winner_str = game.return_winner()
                    store1, store2 = game.get_stores()
                    gui.next_screen(winner_str, store1, store2)

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if (gui.get_screen_index() == 0 or gui.get_screen_index() == 1 or
               gui.get_screen_index() == 3 or gui.get_screen_index() == 4) and \
                    event.type == MOUSEMOTION:
                gui.get_screen().check_hover(pygame.mouse.get_pos())

            if event.type == MOUSEBUTTONDOWN:

                # Main Game Click
                if (gui.get_screen_index() == 2 and
                        (mode == 'TWO' or
                         (mode != 'TWO' and game.get_turn() == 1))):
                    game_gui = gui.get_screen()

                    pit = game_gui.check_click(game.get_turn())
                    if not pit or pit.seeds == 0:
                        continue
                    # remove border
                    for p in game_gui.pits[game.get_turn() - 1]:
                        p.can_select = False
                        p.update_display()
                    game.play_game(game.get_turn(), pit.num)

                    # check if game ended
                    ended = game.get_end_state()
                    # updates gui to new turn after move completed
                    if not ended:
                        game_gui.display_turn(
                            game.get_player_obj().get_name(), game.get_turn())

                    else:
                        # go to end game screen
                        winner_str = game.return_winner()
                        store1, store2 = game.get_stores()
                        gui.next_screen(winner_str, store1, store2)
                        continue

                elif gui.get_screen_index() != 2:
                    click = gui.get_screen().check_click(pygame.mouse.get_pos())

                    # Game Mode Screen Click
                    if click and gui.get_screen_index() == 0:
                        if click == 'INSTRUCTIONS':
                            gui.show_instructions_screen()
                            continue
                        # gui uses mode to determine if pits should be outlined
                        gui.get_game_gui().set_mode(click)
                        mode = click    # loop uses mode to make Ai turn
                        gui.next_screen(click)

                    # Instruction Screen Click
                    if click and gui.get_screen_index() == 4:
                        if click == 'GAME MENU':
                            gui.show_mode_screen()

                    # Player Name Screen Click
                    elif click and gui.get_screen_index() == 1:
                        if click == 'BACK':
                            gui.show_mode_screen()
                        elif len(click) == 2:
                            player_one_name, player_two_name = click
                            game.create_player(player_one_name)
                            game.create_player(player_two_name)
                            gui.next_screen(player_one_name, player_two_name)

                    # End Screen Click
                    elif click and gui.get_screen_index() == 3:
                        # Restart Game
                        if click == 2:
                            game.reset()
                            name1 = name2 = None
                            names = game.get_player_names()
                            if names:
                                name1, name2 = names

                            if not name1:
                                name1 = 'PLAYER 1'
                            if not name2:
                                name2 = 'PLAYER 2'

                            gui.show_new_game_screen(name1, name2)

                        # Go To Main Menu
                        elif click == 1:
                            game.reset(True)
                            gui.get_game_gui().reset()
                            gui.show_mode_screen()

                        # Exit Game
                        elif click == -1:
                            return

            if gui.get_screen_index() == 1 and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    key = -1
                else:
                    key = event.unicode
                gui.get_screen().process_input_change(key)
                pygame.display.flip()


if __name__ == '__main__':
    main()
