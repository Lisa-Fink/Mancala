import pygame
from pygame.locals import *
import pygame.freetype

from Mancala import Mancala

pygame.init()

W_WIDTH = 1200
W_HEIGHT = 800
BOARD_BG = (255, 194, 136)
PIT_BG = (185, 122, 87)
BOARD_TOP = 200
BOARD_LEFT = 100
BOARD_WIDTH = 1000
GAP = 40
PIT_WIDTH = 80
PIT_HEIGHT = 100
STORE_WIDTH = PIT_WIDTH
STORE_HEIGHT = 310
PLAYER2_PIT_TOP = GAP + BOARD_TOP
PLAYER1_PIT_TOP = GAP + BOARD_TOP + STORE_HEIGHT - PIT_HEIGHT
SEED_FONT_COLOR = (0, 0, 0)
FONT = pygame.freetype.SysFont("Arial", 40)


class Hole(pygame.sprite.Sprite):
    def __init__(self, width, height, left, top, seeds=0):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BOARD_BG)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, PIT_BG, self.rect, 0, border_radius=40)
        self.text_rect = self.rect.copy()
        self.text_rect.x = self.text_rect.centerx - 10
        self.text_rect.y = self.text_rect.centery - 15

        self.rect.x = left
        self.rect.y = top
        self.seeds = seeds
        FONT.render_to(self.image, self.text_rect, str(self.seeds))

        self.change = None
        self.time_showing_changed = 0
        self.can_select = False

    def update_display(self):
        self.image.fill(BOARD_BG)
        rect = self.image.get_rect()
        pygame.draw.rect(self.image, PIT_BG, rect, 0, border_radius=40)
        FONT.render_to(self.image, self.text_rect, str(self.seeds))
        if self.change:
            self.display_changed_seed_count(self.change)
        if self.can_select and self.seeds > 0:
            self.select()

    def select(self):
        rect = self.image.get_rect()
        pygame.draw.rect(self.image, (150, 0, 0),
                         rect, 6, border_radius=40)

    def display_changed_seed_count(self, amount):
        sign = ""
        if amount > 0:
            sign = '+'
        change_font = pygame.freetype.SysFont("Arial", 20)
        change_font.render_to(self.image, self.image.get_rect(),
                              sign + str(amount))

    def change_seed_count(self, amount):
        self.change = amount
        self.seeds += amount
        self.time_showing_changed = pygame.time.get_ticks()


class Store(Hole):
    def __init__(self, left, top, player):
        super().__init__(STORE_WIDTH, STORE_HEIGHT, left, top)
        self.player = player


class Pit(Hole):
    def __init__(self, left, top, num):
        super().__init__(PIT_WIDTH, PIT_HEIGHT, left, top, 4)
        self.num = num

class Display:
    def __init__(self, screen):
        self._screen = screen

    def display_title(self):
        font = pygame.font.SysFont('Arial', 64, True)
        text = font.render('Mancala', True, (255, 255, 255))
        self._screen.blit(text, ((W_WIDTH // 2) - text.get_size()[0] // 2,
                                 GAP))

class GUI(Display):
    def __init__(self, screen):
        super().__init__(screen)
        self._change_pits = []
        self.all_sprites = pygame.sprite.Group()
        self.stores = pygame.sprite.Group()
        self.pits = [pygame.sprite.Group(), pygame.sprite.Group()]

        self.initialize_stores()
        self.initialize_pits()
        self.display_title()

    def display_turn(self, name, turn):
        turn_font = pygame.freetype.SysFont("Arial", 30)

        turn_rect = pygame.Rect(10, 100,
                                W_WIDTH // 3, 40)
        pygame.draw.rect(self._screen, (0, 0, 0),
                         turn_rect, 0, 0)

        turn_font.render_to(self._screen, turn_rect, 'Turn: ' + name,
                            (255, 255, 255))

        # add border to pits on players side
        for i in range(len(self.pits)):
            for pit in self.pits[i].sprites():
                if i + 1 == turn:
                    if pit.seeds > 0:
                        pit.can_select = True
                        self.update(pit)
                else:
                    pit.can_select = False
                    self.update(pit)

    def display_board(self):
        pygame.draw.rect(self._screen, BOARD_BG,
                         pygame.Rect(BOARD_LEFT, BOARD_TOP,
                                     BOARD_WIDTH, 400), 0, 140)

    def display_players(self, player1, player2):
        player_font = pygame.freetype.SysFont("Arial", 30)

        player1_rect = pygame.Rect(10, 20,
                                   W_WIDTH // 3, 40)
        player2_rect = pygame.Rect(10, 60,
                                   W_WIDTH // 3, 40)
        pygame.draw.rect(self._screen, (0, 0, 0),
                         player1_rect, 0, 0)
        pygame.draw.rect(self._screen, (0, 0, 0),
                         player2_rect, 0, 0)
        player1_text = 'Player 1: ' + player1
        player2_text = 'Player 2: ' + player2

        player_font.render_to(self._screen, player1_rect, player1_text,
                              (255, 255, 255))
        player_font.render_to(self._screen, player2_rect, player2_text,
                              (255, 255, 255))

    def initialize_stores(self):
        store2 = Store(BOARD_LEFT + GAP, BOARD_TOP + GAP, 2)

        store1 = Store(BOARD_WIDTH + BOARD_LEFT - GAP - STORE_WIDTH,
                       BOARD_TOP + GAP, 1)

        self.stores.add(store1)
        self.stores.add(store2)
        self.all_sprites.add(store1)
        self.all_sprites.add(store2)

    def initialize_pits(self):
        tops = [PLAYER1_PIT_TOP, PLAYER2_PIT_TOP]
        for i in range(6):
            pit = Pit(
                BOARD_LEFT + PIT_WIDTH * i + GAP * (i + 2) + STORE_WIDTH,
                tops[0], i + 1)
            self.pits[0].add(pit)
            self.all_sprites.add(pit)
        # add top row in reverse order
        player2_pits = []
        for i in range(6):
            pit = Pit(
                BOARD_LEFT + PIT_WIDTH * i + GAP * (i + 2) + STORE_WIDTH,
                tops[1], 6 - i)
            # self.pits[0].add(pit)
            player2_pits.append(pit)
            self.all_sprites.add(pit)
        for i in range(len(player2_pits)):
            self.pits[1].add(player2_pits.pop())

    def start_game(self, player1_name, player2_name):
        # Initialise screen
        self.display_title()
        self.display_board()
        self.all_sprites.draw(self._screen)
        self.display_players(player1_name, player2_name)
        self.display_turn(player1_name, 1)

    def update(self, hole):
        hole.update_display()
        self.all_sprites.draw(self._screen)

    def update_pit(self, side, hole_num, amount):
        hole = self.get_pit(side, hole_num)
        hole.change_seed_count(amount)
        self._change_pits.append(hole)
        self.update(hole)
        pygame.display.flip()
        pygame.time.delay(600)

    def remove_change_display(self, hole):
        hole.change = None
        self._change_pits.remove(hole)
        self.update(hole)

    def get_pits_changed(self):
        return self._change_pits

    def detect_pit_click(self, turn):
        for pit in self.pits[turn - 1]:
            if pit.rect.collidepoint(pygame.mouse.get_pos()):
                return pit

    def get_pit(self, side, pit):
        if pit == 7:
            return self.stores.sprites()[side - 1]
        return self.pits[side - 1].sprites()[pit - 1]


class SelectScreen(Display):
    def __init__(self, screen):
        super().__init__(screen)
        self._buttons = []

    def display_button(self, rect, text, offset_x, offset_y, hover=False,
                       add=True):
        button_color = (250, 250, 250)
        if hover:
            button_color = (250, 0, 250)
        pygame.draw.rect(self._screen, button_color, rect,
                         border_radius=10)
        self.display_button_text(rect, text, offset_x, offset_y)
        if add:
            self._buttons.append((rect, text, (offset_x, offset_y)))

    def display_button_text(self, rect, text, offset_x, offset_y):
        font = pygame.font.SysFont('Arial', 28)
        text = font.render(text, True, (0, 0, 0))
        self._screen.blit(text, (rect[0] + offset_x,
                                 rect[1] + offset_y))

    def check_hover(self, mouse_pos):
        for button in self._buttons:
            rect, text, (offset_x, offset_y) = button
            hover = False
            converted = pygame.Rect(rect)
            if converted.collidepoint(mouse_pos):
                hover = True
            self.display_button(rect, text, offset_x, offset_y, hover, False)
            pygame.display.flip()


class StartScreen(SelectScreen):
    BUTTON_WIDTH = 180
    BUTTON_HEIGHT = 60

    TWO_PLAYER_BUTTON = (W_WIDTH // 2 - BUTTON_WIDTH // 2,
                         300, BUTTON_WIDTH, BUTTON_HEIGHT)
    EASY_BUTTON = (W_WIDTH // 2 - BUTTON_WIDTH // 2,
                   400, BUTTON_WIDTH, BUTTON_HEIGHT)
    HARD_BUTTON = (W_WIDTH // 2 - BUTTON_WIDTH // 2,
                   500, BUTTON_WIDTH, BUTTON_HEIGHT)

    START_BUTTON = (W_WIDTH // 2 + 20,
                    600, BUTTON_WIDTH, BUTTON_HEIGHT)
    BACK_BUTTON = (W_WIDTH // 2 - BUTTON_WIDTH - 20,
                    600, BUTTON_WIDTH, BUTTON_HEIGHT)

    INPUT_ONE = (W_WIDTH // 2 - BUTTON_WIDTH, 260,
                 BUTTON_WIDTH * 2, BUTTON_HEIGHT)
    INPUT_TWO = (W_WIDTH // 2 - BUTTON_WIDTH, 420,
                 BUTTON_WIDTH * 2, BUTTON_HEIGHT)

    def __init__(self, screen):
        super().__init__(screen)
        self._mode = None
        self.display_game_mode_screen()
        self._set_game_page = True
        self._player_one_text = ''
        self._player_two_text = ''
        self._game_mode = None

    def display_game_mode_screen(self):
        self._screen.fill((0, 0, 0))
        self._buttons.clear()
        self.display_title()
        self.display_instructions()
        self.display_player_options()

    def display_player_screen(self, game_mode):
        self._screen.fill((0, 0, 0))
        self._buttons.clear()
        self.display_title()
        self.display_player_one_prompt()
        self.display_player_one_input()

        self.display_button(self.START_BUTTON, 'START GAME', 20, 12)
        self.display_button(self.BACK_BUTTON, 'GO BACK', 37, 12)
        if game_mode == 'TWO':
            self.display_player_two_prompt()
            self.display_player_two_input()

    def display_player_one_input(self, active=False, text=None):
        # set data member to remember text when changing active state
        if self._player_one_text and text is None:
            text = self._player_one_text
        else:
            self._player_one_text = text

        input_one_rect = pygame.Rect(self.INPUT_ONE)
        bg = (100, 100, 100)
        if active:
            bg = (200, 200, 200)
        pygame.draw.rect(self._screen, bg,
                         input_one_rect, border_radius=10)
        font = pygame.font.SysFont('Arial', 32)
        text_surface = font.render(text, True, (0, 0, 0))
        # set width so text cannot go outside input_one_rect
        input_one_rect.w = max(100, text_surface.get_width() + 10)
        self._screen.blit(text_surface,
                          (input_one_rect.x + 10, input_one_rect.y + 10))

    def display_player_two_input(self, active=False, text=None):
        # set data member to remember text when changing active state
        if self._player_two_text and text is None:
            text = self._player_two_text
        else:
            self._player_two_text = text

        input_two_rect = pygame.Rect(self.INPUT_TWO)
        bg = (100, 100, 100)
        if active:
            bg = (200, 200, 200)
        pygame.draw.rect(self._screen, bg,
                         input_two_rect, border_radius=10)
        font = pygame.font.SysFont('Arial', 32)
        text_surface = font.render(text, True, (0, 0, 0))
        # set width so text cannot go outside input_one_rect
        input_two_rect.w = max(100, text_surface.get_width() + 10)
        self._screen.blit(text_surface,
                          (input_two_rect.x + 10, input_two_rect.y + 10))

    def display_instructions(self):
        font = pygame.font.SysFont('Arial', 36)
        text = font.render('Please Select a Game Mode', True, (180, 190, 170))
        self._screen.blit(text, (W_WIDTH // 2 - text.get_width() // 2, 200))

    def display_player_one_prompt(self):
        font = pygame.font.SysFont('Arial', 36)
        text = font.render('Please Enter Player One\'s Name',
                           True, (180, 190, 170))
        self._screen.blit(text, (W_WIDTH // 2 - text.get_width() // 2, 200))

    def display_player_two_prompt(self):
        font = pygame.font.SysFont('Arial', 36)
        text = font.render('Please Enter Player Two\'s Name',
                           True, (180, 190, 170))
        self._screen.blit(text, (W_WIDTH // 2 - text.get_width() // 2, 360))

    def display_player_options(self):
        self.display_button(self.TWO_PLAYER_BUTTON, '2 PLAYERS', 30, 12)
        self.display_button(self.EASY_BUTTON, 'VS EASY AI', 30, 12)
        self.display_button(self.HARD_BUTTON, 'VS HARD AI', 30, 12)

    def check_click(self, mouse_pos):
        if self._set_game_page:
            if pygame.Rect(self.EASY_BUTTON).collidepoint(mouse_pos):
                self._set_game_page = False
                self.display_player_screen('EASY')
                self._game_mode = 'AI'
            if pygame.Rect(self.HARD_BUTTON).collidepoint(mouse_pos):
                self._set_game_page = False
                self.display_player_screen('HARD')
                self._game_mode = 'AI'
            if pygame.Rect(self.TWO_PLAYER_BUTTON).collidepoint(mouse_pos):
                self._set_game_page = False
                self.display_player_screen('TWO')
                self._game_mode = 'TWO'
            return self._game_mode

    def check_start_click(self, mouse_pos):
        if pygame.Rect(self.START_BUTTON).collidepoint(mouse_pos):
            return True

    def check_back_click(self, mouse_pos):
        if pygame.Rect(self.BACK_BUTTON).collidepoint(mouse_pos):
            self._game_mode = None
            self._set_game_page = True
            self._player_one_text = self._player_two_text = ''
            self.display_game_mode_screen()
            return True

    def check_input_click(self, mouse_pos):
        if pygame.Rect(self.INPUT_ONE).collidepoint(mouse_pos):
            self.display_player_one_input(True)
            if self._game_mode == 'TWO':
                self.display_player_two_input()
            pygame.display.flip()
            return 1
        else:
            self.display_player_one_input()
            pygame.display.flip()
        if self._game_mode == 'TWO':
            if pygame.Rect(self.INPUT_TWO).collidepoint(mouse_pos):
                self.display_player_two_input(True)
                pygame.display.flip()
                return 2
            else:
                self.display_player_two_input()
                pygame.display.flip()


class EndScreen(SelectScreen):
    BOX_WIDTH = W_WIDTH // 2
    BOX = (W_WIDTH // 4, 240, BOX_WIDTH, W_HEIGHT // 1.5)

    def __init__(self, winner_str, store1, store2):
        super().__init__()
        self.display_box()

    def display_box(self):
        pygame.draw.rect(self._screen, (86, 86, 86), self.BOX,
                         border_radius=10)





def main():
    screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
    pygame.display.set_caption('Mancala')
    start_screen = StartScreen(screen)
    pygame.display.flip()
    gui = GUI(screen)
    game = Mancala(gui)
    # select game mode
    game_screen = 0
    input_1 = False
    player_one = ''
    input_2 = False
    player_two = ''
    game_mode = None

    while True:
        if game_screen == 1 and gui.get_pits_changed():
            cur_time = pygame.time.get_ticks()
            for pit in gui.get_pits_changed():
                if pit.time_showing_changed < cur_time - 1500:
                    gui.remove_change_display(pit)
                    pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if game_screen == 0:
                if event.type == MOUSEMOTION:
                    start_screen.check_hover(pygame.mouse.get_pos())

                if event.type == MOUSEBUTTONDOWN:
                    if not game_mode:
                        game_mode = start_screen.check_click(pygame.mouse.get_pos())
                    else:
                        # check if clicked on back button
                        if start_screen.check_back_click(pygame.mouse.get_pos()):
                            game_mode = None
                            input_1 = input_2 = False
                            player_one = player_two = ''
                            continue
                        # clicked on start game
                        if start_screen.check_start_click(pygame.mouse.get_pos()):
                            if not player_one:
                                player_one = 'PLAYER ONE'
                            if game_mode == 'TWO' and not player_two:
                                player_two = 'PLAYER TWO'
                            game_screen = 1
                            screen.fill((0, 0, 0))
                            game.create_player(player_one)
                            if game_mode == 'EASY':
                                gui.start_game(player_one, -1)
                                game.create_player('0')
                            elif game_mode == 'HARD':
                                gui.start_game(player_one, -1)
                                game.create_player('1')
                            else:
                                gui.start_game(player_one, player_two)
                                game.create_player(player_two)
                        # check if clicked on input
                        else:
                            selected = \
                                start_screen.check_input_click(pygame.mouse.get_pos())
                            if not selected and not input_1 and not input_2:
                                continue
                            if selected == 1:
                                input_1 = True
                                input_2 = False
                            elif game_mode == 'TWO' and selected == 2:
                                input_2 = True
                                input_1 = False
                            else:
                                input_2 = False
                                input_1 = False

                if event.type == pygame.KEYDOWN:
                    if game_mode and (input_1 or input_2):
                        if input_1:
                            if event.key == pygame.K_BACKSPACE:
                                player_one = player_one[:-1]
                            else:
                                player_one += event.unicode
                            start_screen.display_player_one_input(True, player_one)
                            pygame.display.flip()

                        if game_mode == 'TWO' and input_2:
                            if event.key == pygame.K_BACKSPACE:
                                player_two = player_two[:-1]
                            else:
                                player_two += event.unicode
                            start_screen.display_player_two_input(True, player_two)
                            pygame.display.flip()

            # main game
            elif game_screen == 1:
                if event.type == MOUSEBUTTONDOWN:
                    pit = gui.detect_pit_click(game.get_turn())
                    if not pit or pit.seeds == 0:
                        continue
                    # remove border
                    for p in gui.pits[game.get_turn() - 1]:
                        p.can_select = False
                        p.update_display()
                    game.play_game(game.get_turn(), pit.num)
                    # check if game ended
                    ended = game.get_end_state()
                    # updates gui to new turn after move completed
                    if not ended:
                        gui.display_turn(game.get_player_obj().get_name(),
                                         game.get_turn())
                    else:
                        # end game screen
                        game_screen = 2
                        winner_str = game.return_winner()
                        store1, store2 = game.get_stores()
                        end_screen = EndScreen(winner_str, store1, store2)
                        pass

                pygame.display.flip()


if __name__ == '__main__':
    main()
