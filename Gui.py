import pygame
import pygame.freetype

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
FONT = pygame.freetype.Font('Arial.ttf', 38)


class Hole(pygame.sprite.Sprite):
    """
    Represents a hole in the Mancala game board.
    """
    def __init__(self, width, height, left, top, seeds=0):
        """
        Initialize a Hole object.

        Args:
            width (int): The width of the hole.
            height (int): The height of the hole.
            left (int): The x-coordinate of the top-left corner of the hole.
            top (int): The y-coordinate of the top-left corner of the hole.
            seeds (int, optional): The initial number of seeds in the hole. Defaults to 0.
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BOARD_BG)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, PIT_BG, self.rect, 0, border_radius=40)
        self.text_rect = self.rect.copy()
        self.text_rect.x = self.text_rect.centerx - 12
        self.text_rect.y = self.text_rect.centery - 12

        self.rect.x = left
        self.rect.y = top
        self.seeds = seeds
        FONT.render_to(self.image, self.text_rect, str(self.seeds))

        self.change = None
        self.time_showing_changed = 0
        self.can_select = False

    def update_display(self):
        """
         Update the display of the hole on the screen.
        """
        self.image.fill(BOARD_BG)
        rect = self.image.get_rect()
        pygame.draw.rect(self.image, PIT_BG, rect, 0, border_radius=40)
        FONT.render_to(self.image, self.text_rect, str(self.seeds))
        if self.change:
            self.display_changed_seed_count(self.change)
        if self.can_select and self.seeds > 0:
            self.select()

    def select(self):
        """
        Highlight the hole to indicate it can be selected.
        """
        rect = self.image.get_rect()
        pygame.draw.rect(self.image, (150, 0, 0),
                         rect, 6, border_radius=40)

    def display_changed_seed_count(self, amount):
        """
        Display the change in seed count for the hole.

        Args:
            amount (int): The change in seed count.
        """
        sign = ""
        if amount > 0:
            sign = '+'
        change_font = pygame.freetype.Font('Arial.ttf', 18)
        change_font.render_to(self.image, self.image.get_rect(),
                              sign + str(amount))

    def change_seed_count(self, amount):
        """
        Change the seed count in the hole and update the display.

        Args:
            amount (int): The amount to change the seed count by.
        """
        self.change = amount
        pre = self.seeds
        self.seeds += amount

        # adjusts text center if adding a digit
        if pre <= 9 and self.seeds > 9:
            self.text_rect.x -= 8
        elif pre >= 10 and self.seeds < 10:
            self.text_rect.x += 8

        self.time_showing_changed = pygame.time.get_ticks()


class Store(Hole):
    """
    Represents a store in the Mancala game board.
    Inherits from the Hole class.
    """
    def __init__(self, left, top, player):
        """
        Initialize a Store object.

        Args:
            left (int): The x-coordinate of the top-left corner of the store.
            top (int): The y-coordinate of the top-left corner of the store.
            player (int): The player number associated with the store.
        """

        super().__init__(STORE_WIDTH, STORE_HEIGHT, left, top)
        self.player = player


class Pit(Hole):
    """
    Represents a pit in the Mancala game board.
    Inherits from the Hole class.
    """
    def __init__(self, left, top, num):
        """
        Initializes a Pit object.

        Args:
            left (int): The x-coordinate of the top-left corner of the pit.
            top (int): The y-coordinate of the top-left corner of the pit.
            num (int): The number associated with the pit.
        """
        super().__init__(PIT_WIDTH, PIT_HEIGHT, left, top, 4)
        self.num = num


class Display:
    """
    Represents the display of the Mancala game.
    """
    def __init__(self, screen):
        """
        Initialize a Display object.

        Args:
            screen (pygame.Surface): The screen to display the game on.
        """
        self._screen = screen

    def display_title(self):
        """
        Display the title of the game on the screen.
        """
        font = pygame.font.Font('Arial.ttf', 62)
        text = font.render('Mancala', True, (255, 255, 255))
        self._screen.blit(text, ((W_WIDTH // 2) - text.get_size()[0] // 2,
                                 GAP))


class GameScreen(Display):
    """
    Represents the game screen of the Mancala game.
    Inherits from the Display class.
    """
    def __init__(self, screen):
        """
        Initialize a GameScreen object.

        Args:
            screen (pygame.Surface): The screen to display the game on.
        """
        super().__init__(screen)
        self._change_pits = []
        self.all_sprites = pygame.sprite.Group()
        self.stores = pygame.sprite.Group()
        self.pits = [pygame.sprite.Group(), pygame.sprite.Group()]
        self._mode = None

        self.initialize_stores()
        self.initialize_pits()

    def reset(self):
        """
        Reset the game screen by emptying the stores and pits.
        """
        self._change_pits = []
        self.stores.empty()
        self.pits[0].empty()
        self.pits[1].empty()
        self.all_sprites.empty()
        self.initialize_stores()
        self.initialize_pits()

    def set_mode(self, mode):
        """
        Set the game mode.

        Args:
            mode (str): The game mode to set. (TWO, EASY, or HARD)
        """
        self._mode = mode

    def display_turn(self, name, turn):
        """
        Display the current turn on the screen.

        Args:
            name (str): The name of the player whose turn it is.
            turn (int): The current turn number.
        """
        turn_font = pygame.freetype.Font('Arial.ttf', 28)

        turn_rect = pygame.Rect(10, 100,
                                W_WIDTH // 3, 40)
        pygame.draw.rect(self._screen, (0, 0, 0),
                         turn_rect, 0, 0)

        turn_font.render_to(self._screen, turn_rect, 'Turn: ' + name,
                            (255, 255, 255))

        if (self._mode == 'TWO') or (self._mode != 'TWO' and turn == 1):
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
        """
        Display the game board on the screen.
        """
        pygame.draw.rect(self._screen, BOARD_BG,
                         pygame.Rect(BOARD_LEFT, BOARD_TOP,
                                     BOARD_WIDTH, 400), 0, 140)

    def display_players(self, player1, player2):
        """
        Display the names of the players on the screen.

        Args:
            player1 (str): Name of player 1.
            player2 (str): Name of player 2.
        """
        player_font = pygame.freetype.Font('Arial.ttf', 28)

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
        """
        Initialize the stores on the game board.
        """
        store2 = Store(BOARD_LEFT + GAP, BOARD_TOP + GAP, 2)

        store1 = Store(BOARD_WIDTH + BOARD_LEFT - GAP - STORE_WIDTH,
                       BOARD_TOP + GAP, 1)

        self.stores.add(store1)
        self.stores.add(store2)
        self.all_sprites.add(store1)
        self.all_sprites.add(store2)

    def initialize_pits(self):
        """
        Initialize the pits on the game board.
        """
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

    def start(self, player1_name, player2_name):
        """
        Start the game by displaying the initial screen with player names.

        Args:
            player1_name (str): Name of player 1.
            player2_name (str): Name of player 2.
        """
        # Initialise screen
        self._screen.fill((0, 0, 0))
        self.display_title()
        self.display_board()
        self.all_sprites.draw(self._screen)

        # convert AI name to string
        if player2_name == -1:
            player2_name = 'EASY AI'
        if player2_name == -2:
            player2_name = 'HARD AI'

        self.display_players(player1_name, player2_name)
        self.display_turn(player1_name, 1)

    def update(self, hole):
        """
        Update the display after a move is made.

        Args:
            hole (Hole): The hole that was updated.
        """
        hole.update_display()
        self.all_sprites.draw(self._screen)

    def update_pit(self, side, hole_num, amount):
        """
        Update a pit with a new seed count and display the change on the screen.

        Args:
            side (int): The side of the pit (1 for player 1, 2 for player 2).
            hole_num (int): The number of the hole.
            amount (int): The new seed count for the hole.
        """
        hole = self.get_pit(side, hole_num)
        hole.change_seed_count(amount)
        self._change_pits.append(hole)
        self.update(hole)
        pygame.display.flip()
        pygame.time.delay(600)

    def remove_change_display(self, hole):
        """
        Remove the display of seed count change for a hole.

        Args:
            hole (Hole): The hole to remove the change display from.
        """
        hole.change = None
        self._change_pits.remove(hole)
        self.update(hole)

    def get_pits_changed(self):
        """
        Get a list of pits that have changed seed counts.

        Returns:
            list[Hole]: A list of pits with changed seed counts.
        """
        return self._change_pits

    def detect_pit_click(self, turn):
        """
        Detect a pit click on the screen.

        Args:
            turn (int): The current player's turn (1 for player 1, 2 for player 2).

        Returns:
            Hole: The pit that was clicked.
        """
        for pit in self.pits[turn - 1]:
            if pit.rect.collidepoint(pygame.mouse.get_pos()):
                return pit

    def check_click(self, turn):
        """
        Check for a pit click on the screen.

        Args:
            turn (int): The current player's turn (1 for player 1, 2 for player 2).

        Returns:
            Hole: The pit that was clicked, or None if no pit was clicked.
        """
        return self.detect_pit_click(turn)

    def get_pit(self, side, pit):
        """
        Get the pit object based on the side and pit number.

        Args:
            side (int): The side of the pit (1 for player 1, 2 for player 2).
            pit (int): The number of the pit.

        Returns:
            Hole: The pit object.
        """
        if pit == 7:
            return self.stores.sprites()[side - 1]
        return self.pits[side - 1].sprites()[pit - 1]


class SelectScreen(Display):
    """
    Class representing the select screen
    """
    def __init__(self, screen):
        super().__init__(screen)
        self._buttons = []

    def display_button(self, rect, text, offset_x, offset_y, hover=False,
                       add=True):
        """
        Display a button on the screen.

        Args:
            rect (tuple): The dimensions of the button rectangle (x, y, width, height).
            text (str): The text to display on the button.
            offset_x (int): The x offset for the button text.
            offset_y (int): The y offset for the button text.
            hover (bool, optional): Indicates if the button is being hovered over. Defaults to False.
            add (bool, optional): Indicates if the button should be added to the list of buttons. Defaults to True.
        """
        button_color = (250, 250, 250)
        if hover:
            button_color = (250, 0, 250)
        pygame.draw.rect(self._screen, button_color, rect,
                         border_radius=10)
        self.display_button_text(rect, text, offset_x, offset_y)
        if add:
            self._buttons.append((rect, text, (offset_x, offset_y)))

    def display_button_text(self, rect, text, offset_x, offset_y):
        """
        Displays button text on the screen.

        Args:
            rect (tuple): The position and size of the button rectangle.
            text (str): The text to display on the button.
            offset_x (int): The x-axis offset for the text.
            offset_y (int): The y-axis offset for the text.
        """

        font = pygame.font.Font('Arial.ttf', 26)
        text = font.render(text, True, (0, 0, 0))
        self._screen.blit(text, (rect[0] + offset_x,
                                 rect[1] + offset_y))

    def check_hover(self, mouse_pos):
        """
        Checks if the mouse is hovering over any button.

        Args:
            mouse_pos (tuple): The current position of the mouse.

        Returns:
            None
        """
        for button in self._buttons:
            rect, text, (offset_x, offset_y) = button
            hover = False
            converted = pygame.Rect(rect)
            if converted.collidepoint(mouse_pos):
                hover = True
            self.display_button(rect, text, offset_x, offset_y, hover, False)
            pygame.display.flip()


class GameModeScreen(SelectScreen):
    """
    Class representing the game mode selection screen.
    """
    BUTTON_WIDTH = 180
    BUTTON_HEIGHT = 60

    TWO_PLAYER_BUTTON = (W_WIDTH // 2 - BUTTON_WIDTH // 2,
                         300, BUTTON_WIDTH, BUTTON_HEIGHT)
    EASY_BUTTON = (W_WIDTH // 2 - BUTTON_WIDTH // 2,
                   400, BUTTON_WIDTH, BUTTON_HEIGHT)
    HARD_BUTTON = (W_WIDTH // 2 - BUTTON_WIDTH // 2,
                   500, BUTTON_WIDTH, BUTTON_HEIGHT)
    INSTRUCTION_BUTTON = (W_WIDTH // 2 - BUTTON_WIDTH // 2,
                          140, BUTTON_WIDTH, BUTTON_HEIGHT)

    def __init__(self, screen):
        super().__init__(screen)

    def start(self):
        """
        Initializes the game mode selection screen.

        Returns:
            None
        """
        self._screen.fill((0, 0, 0))
        self._buttons.clear()
        self.display_title()
        self.display_instructions()
        self.display_player_options()

    def display_instructions(self):
        """
        Displays the instructions button and text on the screen.

        Returns:
            None
        """
        self.display_button(self.INSTRUCTION_BUTTON, 'How To Play', 20, 14)
        font = pygame.font.Font('Arial.ttf', 34)
        text = font.render('Please Select a Game Mode', True, (180, 190, 170))
        self._screen.blit(text, (W_WIDTH // 2 - text.get_width() // 2, 230))

    def display_player_options(self):
        """
        Displays the player options on the screen.

        Returns:
            None
        """
        self.display_button(self.TWO_PLAYER_BUTTON, '2 PLAYERS', 22, 14)
        self.display_button(self.EASY_BUTTON, 'VS EASY AI', 21, 14)
        self.display_button(self.HARD_BUTTON, 'VS HARD AI', 19, 14)

    def check_click(self, mouse_pos):
        """
        Checks if any button was clicked based on the mouse position.

        Args:
            mouse_pos (tuple): The position of the mouse cursor.

        Returns:
            str or None: The selected game mode or None if no button was clicked.
        """
        if pygame.Rect(self.EASY_BUTTON).collidepoint(mouse_pos):
            return 'EASY'
        if pygame.Rect(self.HARD_BUTTON).collidepoint(mouse_pos):
            return 'HARD'
        if pygame.Rect(self.TWO_PLAYER_BUTTON).collidepoint(mouse_pos):
            return 'TWO'
        if pygame.Rect(self.INSTRUCTION_BUTTON).collidepoint(mouse_pos):
            return 'INSTRUCTIONS'


class InstructionsScreen(SelectScreen):
    """
    Class representing the instructions screen.
    """
    BUTTON_WIDTH = 180
    BUTTON_HEIGHT = 60
    INSTRUCTIONS_IMG = pygame.image.load('instructions.png')
    BACK_BUTTON = (900,
                   20, BUTTON_WIDTH, BUTTON_HEIGHT)

    def __init__(self, screen):
        super().__init__(screen)

    def display_instruction_img(self):
        """
        Displays the instructions image.
        """
        self._screen.blit(self.INSTRUCTIONS_IMG, (0, 0))

    def start(self):
        """
        Displays the instructions screen.
        """
        self._screen.fill((0, 0, 0))
        self.display_instruction_img()
        self.display_button(self.BACK_BUTTON, 'GO BACK', 30, 14)

    def check_click(self, mouse_pos):
        """
        Handles mouse clicks on the screen.

        Args:
            mouse_pos (tuple): The position of the mouse click.

        Returns:
            str: The action to perform based on the click.
        """
        if pygame.Rect(self.BACK_BUTTON).collidepoint(mouse_pos):
            return 'GAME MENU'


class PlayerNameScreen(SelectScreen):
    """
    Class representing the screen for entering player names.
    """
    BUTTON_WIDTH = 180
    BUTTON_HEIGHT = 60

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
        self._active = None
        self._player_one_text = ''
        self._player_two_text = ''
        self._game_mode = None  # 'TWO' or 'EASY' or 'HARD'

    def start(self, game_mode):
        """
        Displays the player name entry screen.

        Args:
            game_mode (str): The selected game mode.
        """
        self._game_mode = game_mode
        self._screen.fill((0, 0, 0))
        self._buttons.clear()
        self.display_title()
        self.display_player_one_prompt()
        self.display_player_one_input()

        self.display_button(self.START_BUTTON, 'START GAME', 8, 14)
        self.display_button(self.BACK_BUTTON, 'GO BACK', 30, 14)

        # resets player one or two text if it was previously set as an int from
        # being an Ai. Otherwise, raises an error when displaying input box
        if isinstance(self._player_two_text, int):
            self._player_two_text = ''
        if isinstance(self._player_one_text, int):
            self._player_one_text = ''

        if game_mode == 'TWO':
            self.display_player_two_prompt()
            self.display_player_two_input()

    def process_input_change(self, char):
        """
        Handles changes in the input text.

        Args:
            char (str or int): The entered character or -1 for backspace.
        """
        if self._active is None:
            return
        # set data member to remember text when changing active state
        if self._active == 1:
            if char == -1:
                self._player_one_text = self._player_one_text[:-1]
            else:
                self._player_one_text += char
        elif self._active == 2:
            if char == -1:
                self._player_two_text = self._player_two_text[:-1]
            else:
                self._player_two_text += char
        self.display_player_one_input()
        if self._game_mode == 'TWO':
            self.display_player_two_input()

    def display_player_one_input(self):
        """
        Displays the input box for player one.
        """
        input_one_rect = pygame.Rect(self.INPUT_ONE)
        bg = (100, 100, 100)
        if self._active == 1:
            bg = (200, 200, 200)
        pygame.draw.rect(self._screen, bg,
                         input_one_rect, border_radius=10)
        font = pygame.font.Font('Arial.ttf', 30)
        text_surface = font.render(self._player_one_text, True, (0, 0, 0))
        # set width so text cannot go outside input_one_rect
        input_one_rect.w = max(100, text_surface.get_width() + 10)
        self._screen.blit(text_surface,
                          (input_one_rect.x + 10, input_one_rect.y + 10))

    def display_player_two_input(self):
        """
        Displays the input box for player two.
        """
        input_two_rect = pygame.Rect(self.INPUT_TWO)
        bg = (100, 100, 100)
        if self._active == 2:
            bg = (200, 200, 200)
        pygame.draw.rect(self._screen, bg,
                         input_two_rect, border_radius=10)
        font = pygame.font.Font('Arial.ttf', 30)
        text_surface = font.render(self._player_two_text, True, (0, 0, 0))
        # set width so text cannot go outside input_one_rect
        input_two_rect.w = max(100, text_surface.get_width() + 10)
        self._screen.blit(text_surface,
                          (input_two_rect.x + 10, input_two_rect.y + 10))

    def display_player_one_prompt(self):
        """
        Displays the prompt for entering player one's name.
        """
        font = pygame.font.Font('Arial.ttf', 34)
        text = font.render('Please Enter Player One\'s Name',
                           True, (180, 190, 170))
        self._screen.blit(text, (W_WIDTH // 2 - text.get_width() // 2, 200))

    def display_player_two_prompt(self):
        """
        Displays the prompt for entering player two's name.
        """
        font = pygame.font.Font('Arial.ttf', 34)
        text = font.render('Please Enter Player Two\'s Name',
                           True, (180, 190, 170))
        self._screen.blit(text, (W_WIDTH // 2 - text.get_width() // 2, 360))

    def check_click(self, mouse_pos):
        """
        Handles mouse clicks on the screen.

        Args:
            mouse_pos (tuple): The position of the mouse click.

        Returns:
            str or tuple: The action to perform based on the click.
        """
        # clicked start
        if pygame.Rect(self.START_BUTTON).collidepoint(mouse_pos):
            # handle returning AI type
            if self._game_mode == 'EASY':
                self._player_two_text = -1
            if self._game_mode == 'HARD':
                self._player_two_text = -2

            # handle empty input
            if not self._player_one_text:
                self._player_one_text = 'PLAYER 1'
            if not self._player_two_text:
                self._player_two_text = 'PLAYER 2'
            return self._player_one_text, self._player_two_text
        # clicked back
        if pygame.Rect(self.BACK_BUTTON).collidepoint(mouse_pos):
            return 'BACK'

        # check input clicks
        if pygame.Rect(self.INPUT_ONE).collidepoint(mouse_pos):
            self._active = 1
        elif (self._game_mode == 'TWO' and
              pygame.Rect(self.INPUT_TWO).collidepoint(mouse_pos)):
            self._active = 2
        else:
            self._active = None
        self.display_player_one_input()
        if self._game_mode == 'TWO':
            self.display_player_two_input()
        pygame.display.flip()


class EndScreen(SelectScreen):
    """
    Class representing the end screen.
    """

    BOX_WIDTH = W_WIDTH // 2
    BOX = (W_WIDTH // 4, 160, BOX_WIDTH, W_HEIGHT // 1.5)

    BUTTON_WIDTH = 180
    BUTTON_HEIGHT = 60
    BUTTON_X = W_WIDTH // 2 - BUTTON_WIDTH // 2

    AGAIN_BUTTON = (BUTTON_X, BOX[1] + 245, BUTTON_WIDTH, BUTTON_HEIGHT)
    MENU_BUTTON = (BUTTON_X, BOX[1] + 325, BUTTON_WIDTH, BUTTON_HEIGHT)
    QUIT_BUTTON = (BUTTON_X, BOX[1] + 405, BUTTON_WIDTH, BUTTON_HEIGHT)

    def __init__(self, screen):
        super().__init__(screen)

    def start(self, winner_str, store1, store2):
        """
        Displays the end screen.

        Args:
            winner_str (str): The string indicating the winner.
            store1 (int): The number of seeds in Player 1's store.
            store2 (int): The number of seeds in Player 2's store.

        Returns:
            None
        """
        self.display_title()
        self.display_box()

        # text
        self.display_winner_text(winner_str, 45)
        self.display_winner_text('Player 1: ' + str(store1) + ' seeds', 105)
        self.display_winner_text('Player 2: ' + str(store2) + ' seeds', 165)

        # buttons
        self.display_button(self.AGAIN_BUTTON, 'PLAY AGAIN', 18, 14)
        self.display_button(self.MENU_BUTTON, 'MAIN MENU', 18, 14)
        self.display_button(self.QUIT_BUTTON, 'EXIT GAME', 22, 14)

    def display_winner_text(self, winner_str, offset_y):
        """
        Displays the winner text.

        Args:
            winner_str (str): The string to display.
            offset_y (int): The vertical offset for positioning.

        Returns:
            None
        """
        font = pygame.font.Font('Arial.ttf', 34)
        text = font.render(winner_str, True, (180, 190, 170))
        self._screen.blit(text, (self.BOX[0] + 45, self.BOX[1] + offset_y))

    def display_box(self):
        """
        Displays the box with the end of game text/options.
        """
        pygame.draw.rect(self._screen, (86, 86, 86), self.BOX,
                         border_radius=10)

    def check_click(self, mouse_pos):
        """
        Handles mouse clicks on the screen.

        Args:
            mouse_pos (tuple): The position of the mouse click.

        Returns:
            int: The action to perform based on the click. 2 is play again,
                1 is go to menu, -1 is quit.
        """
        # clicked on play again
        if pygame.Rect(self.AGAIN_BUTTON).collidepoint(mouse_pos):
            return 2
        if pygame.Rect(self.MENU_BUTTON).collidepoint(mouse_pos):
            return 1
        if pygame.Rect(self.QUIT_BUTTON).collidepoint(mouse_pos):
            return -1


class GraphicInterface:
    """
    Class representing the graphic interface for the Mancala game.
    """
    def __init__(self):
        self._screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
        self._select_mode_screen = GameModeScreen(self._screen)
        self._player_screen = PlayerNameScreen(self._screen)
        self._game_screen = GameScreen(self._screen)
        self._end_screen = EndScreen(self._screen)
        self._instructions = InstructionsScreen(self._screen)
        self._screens = [self._select_mode_screen, self._player_screen,
                         self._game_screen, self._end_screen,
                         self._instructions]

        self._current_screen = 0
        pygame.display.set_caption('Mancala')

        # starts with select game mode screen
        self._select_mode_screen.start()
        pygame.display.flip()

    def next_screen(self, *args):
        """
        Moves to the next screen.

        Args:
            *args: Optional arguments to pass to the next screen.

        Returns:
            None
        """
        if self._current_screen < 4:
            self._current_screen += 1
        else:
            self._current_screen = 0
        self._screens[self._current_screen].start(*args)
        pygame.display.flip()

    def get_game_gui(self):
        """
        Returns the GameScreen instance.
        """
        return self._game_screen

    def get_screen_index(self):
        """
        Returns the index of the current screen.
        """
        return self._current_screen

    def get_screen(self):
        """
        Returns the current screen.
        """
        return self._screens[self._current_screen]

    def show_mode_screen(self):
        """
        Displays the game mode selection screen.
        """
        self._current_screen = 0
        self._select_mode_screen.start()
        pygame.display.flip()

    def game_gui_showing_changed(self):
        """
        Checks if the game GUI is showing.

        Returns:
            bool: True if the game GUI is showing, False otherwise.
        """
        return len(self._game_screen.get_pits_changed()) > 0

    def show_game_screen(self, name1, name2):
        """
        Displays the game screen.

        Args:
            name1 (str): The name of Player 1.
            name2 (str): The name of Player 2.

        Returns:
            None
        """
        self._current_screen = 2
        self._game_screen.start(name1, name2)
        pygame.display.flip()

    def show_new_game_screen(self, name1, name2):
        """
        Displays a new game screen.

        Args:
            name1 (str): The name of Player 1.
            name2 (str): The name of Player 2.

        Returns:
            None
        """
        self._game_screen.reset()
        self.show_game_screen(name1, name2)
        pygame.display.flip()

    def show_instructions_screen(self):
        """
        Displays the instructions screen.
        """
        self._current_screen = 4
        self._instructions.start()
        pygame.display.flip()
