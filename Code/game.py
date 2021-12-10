from os import system
import pygame
import thorpy
from pygame.constants import FULLSCREEN, RESIZABLE
from board import Board
from player_turn import player_turn


class GameManager:
    def __init__(self):
        self.init()
        self.init_ui()

    def init(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("test program")
        self.screen = pygame.display.set_mode((800, 800), RESIZABLE)
        self.running = True
        background = pygame.image.load("Assets//background.jpg")
        self.board = Board(background=background, size=19, font_path="MONOFONT.ttf",
                           piece_sound_effect_path="Assets//Sounds//place_piece.ogg")
        self.clock = pygame.time.Clock()
        self.current_colour = player_turn.BLACK
        self.time_delta = 0

    def init_ui(self):
        self.slider = thorpy.SliderX(100, (12, 35), "My Slider")
        self.button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
        self.box = thorpy.Box(elements=[self.slider, self.button])
        # we regroup all elements on a menu, even if we do not launch the menu
        self.menu = thorpy.Menu(self.box)
        # important : set the screen as surface for all elements
        for element in self.menu.get_population():
            element.surface = self.screen
        # use the elements normally...

    def run(self):
        while self.running:
            self.time_delta = self.clock.tick(60) / 1000.0
            self.process_events()
            self.render()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.resize_window()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.place_piece()
            self.menu.react(event)

    def place_piece(self):
        placed_piece = self.board.check_mouse_position(pygame.mouse.get_pos(), self.current_colour)
        if placed_piece:
            if self.current_colour is player_turn.BLACK:
                self.current_colour = player_turn.WHITE
            elif self.current_colour is player_turn.WHITE:
                self.current_colour = player_turn.BLACK
                
    def resize_window(self, event):
        width, height = event.size
        if width < 800:
            width = 800
        if height < 800:
            height = 800
        self.screen = pygame.display.set_mode((width, height), RESIZABLE)

    def render(self):
        self.board.render(self.screen)
        self.box.set_topleft((100, 100))
        # box.blit()
        # box.update()
        pygame.display.flip()
