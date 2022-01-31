import sys
from os import system
import pygame
import thorpy
from pygame.constants import FULLSCREEN, RESIZABLE
from board import Board
from colours import Colour
from monte_carlo_tree_search import MonteCarloTreeSearch
from playerturn import PlayerTurn
from minimax import *


class GameManager:
    def __init__(self):
        self.init()
        self.init_ui()

    def init(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Monte Carlo Tree Search")
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)
        self.running = True
        background = pygame.image.load("Assets//background.jpg")
        self.board = Board(background=background, size=19, font_path="MONOFONT.ttf",
                           piece_sound_effect_path="Assets//Sounds//place_piece.ogg")
        self.clock = pygame.time.Clock()
        self.current_colour = PlayerTurn.BLACK
        self.time_delta = 0
        self.has_passed = False
        self.game_running = False
        self.game_over = False

    def pass_func(self):
        if self.has_passed:
            self.game_running = False
            self.game_over = True
        self.has_passed = True
        if self.current_colour is PlayerTurn.BLACK:
            self.current_colour = PlayerTurn.WHITE
        elif self.current_colour is PlayerTurn.WHITE:
            self.current_colour = PlayerTurn.BLACK

    def start_game(self):
        self.game_running = True

    def init_ui(self):
        self.button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
        self.pass_button = thorpy.make_button("Pass", func=self.pass_func)
        self.box = thorpy.Box(elements=[self.button, self.pass_button])
        # we regroup all elements on a menu, even if we do not launch the menu
        self.menu = thorpy.Menu(self.box)
        # important : set the screen as surface for all elements
        for element in self.menu.get_population():
            element.surface = self.screen
        # use the elements normally...

        self.play_game = thorpy.make_button("Play Game", func=self.start_game)
        self.main_menu_box = thorpy.Box(elements=[self.play_game])
        self.main_menu = thorpy.Menu(self.main_menu_box)

    def run(self):
        while self.running:
            self.time_delta = self.clock.tick(60) / 1000.0
            self.update()
            self.process_events()
            self.render()

    def update(self):
        if self.game_running:
            rules = GoRules(self.board.piece_matrix, self.board.size)
            moves = rules.get_legal_spots_to_play(self.board.piece_matrix)
            colour = Colour.BLACK if self.current_colour == PlayerTurn.BLACK else Colour.WHITE
            if len(moves) > 0:
                monte_carlo = MonteCarloTreeSearch(self.board, colour)
                position = monte_carlo.get_best_move_in_time(self.board)
                print(position)
                self.board.place_piece_at_position(self.current_colour, position.position)
                self.current_colour = PlayerTurn.WHITE if self.current_colour is PlayerTurn.BLACK else PlayerTurn.BLACK


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.resize_window(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.game_running:
                pass
                #self.place_piece()
            if self.game_running:
                self.menu.react(event)
            elif not self.game_over:
                self.main_menu.react(event)
                
    def place_piece(self):
        placed_piece = self.board.check_mouse_position(pygame.mouse.get_pos(), self.current_colour)
        if placed_piece:
            self.has_passed = False
            if self.current_colour is PlayerTurn.BLACK:
                self.current_colour = PlayerTurn.WHITE
            elif self.current_colour is PlayerTurn.WHITE:
                self.current_colour = PlayerTurn.BLACK
            monte_carlo = MonteCarloTreeSearch(self.board, Colour.WHITE)
            position = monte_carlo.get_best_move_in_time(self.board).position
            print(position)
            self.board.place_piece_at_position(PlayerTurn.WHITE, position)
        #minimax = MiniMax(3)
        #alpha = -100000
        #beta = 100000
        #minimax.do_move_in_time(alpha, beta, state=self.board, depth=0, move=None, is_minimiser=False,
                                #player_colour=Colour.WHITE)
        print("Placed piece")
        if placed_piece:
            self.has_passed = False
            if self.current_colour is PlayerTurn.BLACK:
                self.current_colour = PlayerTurn.WHITE
            elif self.current_colour is PlayerTurn.WHITE:
                self.current_colour = PlayerTurn.BLACK
                
    def resize_window(self, event):
        width, height = event.size
        if width < self.width:
            width = self.width
        if height < self.height:
            height = self.height
        self.screen = pygame.display.set_mode((width, height), RESIZABLE)

    def render(self):
        if self.game_running:
            self.board.render(self.screen)
            self.box.set_topleft((self.width - 225, 100))
            self.box.blit()
            self.box.update()
        elif not self.game_over:
            self.main_menu_box.set_topleft((self.width / 2, self.height / 2))
            self.main_menu_box.blit()
            self.main_menu_box.update()

        pygame.display.flip()
