import sys
from os import system
import pygame
import thorpy
from pygame.constants import FULLSCREEN, RESIZABLE
from board import Board
from colours import Colour
from monte_carlo_tree_search import MonteCarloTreeSearch
from player_type import PlayerType
from playerturn import PlayerTurn
from minimax import *


def react_func(event):
    print("Hello")


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
        self.board = Board(
            background=background,
            size=5,
            font_path="MONOFONT.ttf",
            piece_sound_effect_path="Assets//Sounds//place_piece.ogg",
        )
        self.clock = pygame.time.Clock()
        self.current_colour = PlayerTurn.BLACK
        self.time_delta = 0
        self.has_passed = False
        self.game_running = False
        self.game_over = False

    """
    checks if both of the players passed in a row, if they did then the game is over
    """

    def pass_func(self):
        if self.has_passed:
            self.game_running = False
            self.game_over = True
        self.has_passed = True
        if self.current_colour is PlayerTurn.BLACK:
            self.current_colour = PlayerTurn.WHITE
        elif self.current_colour is PlayerTurn.WHITE:
            self.current_colour = PlayerTurn.BLACK

    """
    sets up the players for both black and white
    makes sure to use the correct ai or actual player for both players based on what radio button was pressed
    """

    def start_game(self):
        self.game_running = True
        selected = self.radio_pool.get_selected()
        if selected == self.player_button:
            print("Player is player one")
            self.player_player1 = True
        elif selected == self.monte_carlo_button:
            print("Minimax is player one")
            self.monte_carlo_player1 = True
        elif selected == self.alpha_beta_button:
            print("Alpha beta is player one")
            self.alpha_beta_player1 = True

        player_two = self.player2_radio_pool.get_selected()
        if player_two == self.player2_button:
            self.player_player2 = True
        elif player_two == self.monte_carlo2_button:
            self.monte_carlo_player2 = True
        elif player_two == self.alpha_beta2_button:
            self.alpha_beta_player2 = True

    """
    Creates all of the different UI buttons for the main menu screen. This lets you start the game 
    as well as deciding what ai you want to play against or play against someone else or wathc the ai play.
    """

    def init_ui(self):
        self.button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
        self.pass_button = thorpy.make_button("Pass", func=self.pass_func)
        self.box = thorpy.Box(elements=[self.button, self.pass_button])
        self.menu = thorpy.Menu(self.box)
        for element in self.menu.get_population():
            element.surface = self.screen

        self.play_game = thorpy.make_button("Play Game", func=self.start_game)
        self.player_button = thorpy.Checker("Player", type_="radio")
        self.monte_carlo_button = thorpy.Checker("Monte Carlo", type_="radio")
        self.alpha_beta_button = thorpy.Checker("Alpha Beta", type_="radio")
        self.player_player1 = False
        self.monte_carlo_player1 = False
        self.alpha_beta_player1 = False
        self.player_player2 = False
        self.monte_carlo_player2 = False
        self.alpha_beta_player2 = False
        self.radio_pool = thorpy.RadioPool(
            [
                self.player_button,
                self.monte_carlo_button,
                self.alpha_beta_button,
            ],
            first_value=self.player_button,
        )
        self.player2_button = thorpy.Checker("Player", type_="radio")
        self.monte_carlo2_button = thorpy.Checker("Monte Carlo", type_="radio")
        self.alpha_beta2_button = thorpy.Checker("Alpha Beta", type_="radio")
        self.player2_radio_pool = thorpy.RadioPool(
            [
                self.player2_button,
                self.monte_carlo2_button,
                self.alpha_beta2_button,
            ],
            first_value=self.player2_button,
        )
        self.text = thorpy.Element(text="Player 1")
        self.player2 = thorpy.Element(text="Player 2")
        self.main_menu_box = thorpy.Box(
            elements=[
                self.play_game,
                self.text,
                self.player_button,
                self.monte_carlo_button,
                self.alpha_beta_button,
                self.player2,
                self.player2_button,
                self.monte_carlo2_button,
                self.alpha_beta2_button,
            ]
        )
        self.main_menu_box.center()
        self.background = thorpy.Background(
            image="Assets/background.jpg", elements=[self.main_menu_box]
        )
        self.main_menu = thorpy.Menu(elements=self.background, fps=60)

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
            colour = (
                Colour.BLACK
                if self.current_colour == PlayerTurn.BLACK
                else Colour.WHITE
            )
            if len(moves) > 0:
                monte_carlo = MonteCarloTreeSearch(self.board, colour)
                alpha_beta = MiniMax(4, self.board.size)

                is_maximiser = (
                    True if self.current_colour is PlayerTurn.BLACK else False
                )
                played_move = False

                if (
                    self.current_colour is PlayerTurn.BLACK and self.alpha_beta_player1
                ) or (
                    self.current_colour is PlayerTurn.WHITE and self.alpha_beta_player2
                ):
                    position = alpha_beta.get_best_move_in_time(
                        deepcopy(self.board.piece_matrix),
                        is_maximiser=is_maximiser,
                    )
                    played_move = True
                elif (
                    self.current_colour is PlayerTurn.BLACK and self.monte_carlo_player1
                ) or (
                    self.current_colour is PlayerTurn.WHITE and self.monte_carlo_player2
                ):
                    position = monte_carlo.get_best_move_in_time(self.board)
                    played_move = True

                if played_move:
                    print(position)

                    self.board.place_piece_at_position(
                        self.current_colour, position.position
                    )
                    self.current_colour = (
                        PlayerTurn.WHITE
                        if self.current_colour is PlayerTurn.BLACK
                        else PlayerTurn.BLACK
                    )

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.resize_window(event)
            elif (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.game_running
            ):
                if (
                    self.current_colour is PlayerTurn.BLACK
                    and self.player_player1
                    or self.current_colour is PlayerTurn.WHITE
                    and self.player_player2
                ):
                    self.place_piece()
            if self.game_running:
                self.menu.react(event)
            elif not self.game_over:
                self.main_menu.react(event)

    def place_piece(self):
        placed_piece = self.board.check_mouse_position(
            pygame.mouse.get_pos(), self.current_colour
        )
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
            self.background.blit()
            self.main_menu_box.set_topleft((self.width / 2 - 50, self.height / 2 - 50))
            self.main_menu_box.blit()
            self.main_menu_box.update()

        pygame.display.flip()
