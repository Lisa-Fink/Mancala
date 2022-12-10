import pygame
from pygame.locals import *
import pygame.freetype

from Gui import GraphicInterface
from Mancala import Mancala


def check_display_time(gui):
    cur_time = pygame.time.get_ticks()
    for pit in gui.get_pits_changed():
        if pit.time_showing_changed < cur_time - 1500:
            gui.remove_change_display(pit)
            pygame.display.flip()


def main():
    gui = GraphicInterface()
    game = Mancala(gui.get_game_gui())

    while True:
        # check if on game screen and there are pits showing changed amount
        if gui.get_screen_index() == 2 and gui.game_gui_showing_changed():
            # removes update if passed time limit
            check_display_time(gui.get_game_gui())

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if (gui.get_screen_index() == 0 or gui.get_screen_index() == 1 or
               gui.get_screen_index() == 3) and event.type == MOUSEMOTION:
                gui.get_screen().check_hover(pygame.mouse.get_pos())

            if event.type == MOUSEBUTTONDOWN:

                # Main Game Click
                if gui.get_screen_index() == 2:
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
                        gui.next_screen(click)

                    # Player Name Screen Click
                    elif click and gui.get_screen_index() == 1:
                        if click == 'BACK':
                            gui.show_mode_screen()
                        else:
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
