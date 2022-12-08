import pygame
from pygame.locals import *
import pygame.freetype

from Mancala import Mancala

pygame.init()


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
        self.text_rect = self.rect.copy().center

        self.rect.x = left
        self.rect.y = top
        self.seeds = seeds
        FONT.render_to(self.image, self.text_rect, str(self.seeds))

        self.change = None
        self.time_showing_changed = 0

    def update_display(self):
        self.image.fill(BOARD_BG)
        rect = self.image.get_rect()
        pygame.draw.rect(self.image, PIT_BG, rect, 0, border_radius=40)
        FONT.render_to(self.image, self.text_rect, str(self.seeds))
        if self.change:
            self.display_changed_seed_count(self.change)

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


class GUI:
    def __init__(self):
        self._change_pits = []

        self.screen = pygame.display.set_mode((1200, 800))
        self.board = pygame.draw.rect(self.screen, BOARD_BG,
                                      pygame.Rect(BOARD_LEFT, BOARD_TOP,
                                                   BOARD_WIDTH, 400), 0, 140)
        self.all_sprites = pygame.sprite.Group()
        self.stores = pygame.sprite.Group()
        self.pits = [pygame.sprite.Group(), pygame.sprite.Group()]

        store2 = Store(BOARD_LEFT + GAP, BOARD_TOP + GAP, 2)

        store1 = Store(BOARD_WIDTH + BOARD_LEFT - GAP - STORE_WIDTH,
                       BOARD_TOP + GAP, 1)

        self.stores.add(store1)
        self.stores.add(store2)
        self.all_sprites.add(store1)
        self.all_sprites.add(store2)

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

    def start(self):
        # Initialise screen
        pygame.display.set_caption('Mancala')
        self.all_sprites.draw(self.screen)

    def update(self, hole):
        hole.update_display()
        self.all_sprites.draw(self.screen)

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


def main():
    gui = GUI()
    gui.start()
    game = Mancala(gui)
    game.create_player('Lisa')
    game.create_player('Layla')
    pygame.display.flip()

    # Event loop

    while True:
        cur_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == MOUSEBUTTONDOWN and pygame.Rect.collidepoint(
                    gui.board, pygame.mouse.get_pos()):
                pit = gui.detect_pit_click(game.get_turn())
                if not pit:
                    continue
                game.play_game(game.get_turn(), pit.num)

        if gui.get_pits_changed():
            for pit in gui.get_pits_changed():
                if pit.time_showing_changed < cur_time - 1500:
                    gui.remove_change_display(pit)

        pygame.display.flip()


if __name__ == '__main__':
    main()
