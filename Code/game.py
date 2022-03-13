import sys
from os import system
import pygame
import thorpy
from pygame.constants import FULLSCREEN, RESIZABLE
from board import Board
from colours import Colour
from databaseCRUD import *
from database_move import DatabaseMove
from database_game import DatabaseGame
from monte_carlo_tree_search import MonteCarloTreeSearch
from player_type import PlayerType
from playerturn import PlayerTurn
from minimax import *


def react_func(event):
    print("Hello")


class GameManager:
    def __init__(self):
        self.sent_game_data = False
        self.player1_text = ""
        self.player2_text = ""
        self.player1_captures = 0
        self.player2_captures = 0
        self.init()
        self.init_ui()
        self.calculation_time = 5

    def init(self):
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption(
            "Monte Carlo Tree Search"
        )
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode(
            (self.width, self.height), RESIZABLE
        )
        self.running = True
        background = pygame.image.load(
            "Assets//background.jpg"
        )
        self.board_size = 5
        self.board = Board(
            background=background,
            size=self.board_size,
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
            self.player_player1 = True
            self.player1_text = "Player"
        elif selected == self.monte_carlo_button:
            self.monte_carlo_player1 = True
            self.player1_text = "MonteCarlo"
        elif selected == self.alpha_beta_button:
            self.alpha_beta_player1 = True
            self.player1_text = "AlphaBeta"

        player_two = self.player2_radio_pool.get_selected()
        if player_two == self.player2_button:
            self.player_player2 = True
            self.player2_text = "Player"
        elif player_two == self.monte_carlo2_button:
            self.monte_carlo_player2 = True
            self.player2_text = "MonteCarlo"
        elif player_two == self.alpha_beta2_button:
            self.alpha_beta_player2 = True
            self.player2_text = "AlphaBeta"

        time_allocated = self.time_radio_pool.get_selected()
        if time_allocated == self.five_seconds_button:
            self.calculation_time = 5
        elif time_allocated == self.fifteen_seconds_button:
            self.calculation_time = 15
        elif time_allocated == self.twenty_seconds_button:
            self.calculation_time = 20

        board_size = self.board_size_pool.get_selected()
        if board_size == self.five_by_five_board:
            self.create_board(5)
        elif board_size == self.nine_by_nine_board:
            self.create_board(9)
        elif board_size == self.thirteen_by_thirteen_board:
            self.create_board(13)
        elif board_size == self.nineteen_by_nineteen_board:
            self.create_board(19)

    def create_board(self, size):
        self.board_size = size
        background = pygame.image.load(
            "Assets//background.jpg"
        )
        self.board = Board(
            background=background,
            size=self.board_size,
            font_path="MONOFONT.ttf",
            piece_sound_effect_path="Assets//Sounds//place_piece.ogg",
        )

    """
    Creates all of the different UI buttons for the main menu screen. This lets you start the game 
    as well as deciding what ai you want to play against or play against someone else or wathc the ai play.
    """

    def init_ui(self):
        self.button = thorpy.make_button(
            "Quit", func=thorpy.functions.quit_func
        )
        self.pass_button = thorpy.make_button(
            "Pass", func=self.pass_func
        )
        self.box = thorpy.Box(
            elements=[self.button, self.pass_button]
        )
        self.menu = thorpy.Menu(self.box)
        for element in self.menu.get_population():
            element.surface = self.screen

        self.play_game = thorpy.make_button(
            "Play Game", func=self.start_game
        )
        self.player_button = thorpy.Checker(
            "Player", type_="radio"
        )
        self.monte_carlo_button = thorpy.Checker(
            "Monte Carlo", type_="radio"
        )
        self.alpha_beta_button = thorpy.Checker(
            "Alpha Beta", type_="radio"
        )
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
        self.player2_button = thorpy.Checker(
            "Player", type_="radio"
        )
        self.monte_carlo2_button = thorpy.Checker(
            "Monte Carlo", type_="radio"
        )
        self.alpha_beta2_button = thorpy.Checker(
            "Alpha Beta", type_="radio"
        )
        self.player2_radio_pool = thorpy.RadioPool(
            [
                self.player2_button,
                self.monte_carlo2_button,
                self.alpha_beta2_button,
            ],
            first_value=self.player2_button,
        )

        self.five_seconds_button = thorpy.Checker("5", type_="radio")
        self.fifteen_seconds_button = thorpy.Checker("15", type_="radio")
        self.twenty_seconds_button = thorpy.Checker("20", type_="radio")

        self.time_radio_pool = thorpy.RadioPool([self.five_seconds_button, self.fifteen_seconds_button, self.twenty_seconds_button], first_value=self.five_seconds_button)

        self.five_by_five_board = thorpy.Checker("5x5", type_="radio")
        self.nine_by_nine_board = thorpy.Checker("9x9", type_="radio")
        self.thirteen_by_thirteen_board = thorpy.Checker("13x13", type_="radio")
        self.nineteen_by_nineteen_board = thorpy.Checker("19x19", type_="radio")

        self.board_size_pool = thorpy.RadioPool([self.five_by_five_board, self.nine_by_nine_board, self.thirteen_by_thirteen_board, self.nineteen_by_nineteen_board],
                                                first_value=self.five_by_five_board)

        self.text = thorpy.Element(text="Player 1")
        self.player2 = thorpy.Element(text="Player 2")
        self.time_limit = thorpy.Element(text="Time Limit")
        self.board_size_text = thorpy.Element(text="Board Size")

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
                self.time_limit,
                self.five_seconds_button,
                self.fifteen_seconds_button,
                self.twenty_seconds_button,
                self.board_size_text,
                self.five_by_five_board,
                self.nine_by_nine_board,
                self.thirteen_by_thirteen_board,
                self.nineteen_by_nineteen_board,
            ]
        )
        self.main_menu_box.center()
        self.background = thorpy.Background(
            image="Assets/background.jpg",
            elements=[self.main_menu_box],
        )
        self.main_menu = thorpy.Menu(
            elements=self.background, fps=60
        )

    def run(self):
        while self.running:
            self.time_delta = self.clock.tick(60) / 1000.0
            self.update()
            self.process_events()
            self.render()

    def update(self):
        if self.game_running:
            rules = GoRules(
                self.board.piece_matrix, self.board.size
            )
            moves = rules.get_legal_spots_to_play(
                self.board.piece_matrix
            )
            colour = (
                Colour.BLACK
                if self.current_colour == PlayerTurn.BLACK
                else Colour.WHITE
            )

            database_colour = (
                "Black"
                if self.current_colour == PlayerTurn.BLACK
                else "White"
            )
            player_type = ""
            moves_calculated = 0

            if len(moves) > 0:
                monte_carlo = MonteCarloTreeSearch(
                    self.board, colour
                )
                monte_carlo.calculation_time = self.calculation_time
                alpha_beta = MiniMax(4, self.board.size)
                alpha_beta.calculation_time = self.calculation_time

                is_maximiser = (
                    True
                    if self.current_colour
                    is PlayerTurn.BLACK
                    else False
                )
                played_move = False

                if (
                    self.current_colour is PlayerTurn.BLACK
                    and self.alpha_beta_player1
                ) or (
                    self.current_colour is PlayerTurn.WHITE
                    and self.alpha_beta_player2
                ):
                    position = (
                        alpha_beta.get_best_move_in_time(
                            deepcopy(
                                self.board.piece_matrix
                            ),
                            is_maximiser=is_maximiser,
                        )
                    )
                    played_move = True
                    player_type = "AlphaBeta"
                    moves_calculated = (
                        alpha_beta.get_moves_calculated()
                    )
                elif (
                    self.current_colour is PlayerTurn.BLACK
                    and self.monte_carlo_player1
                ) or (
                    self.current_colour is PlayerTurn.WHITE
                    and self.monte_carlo_player2
                ):
                    position = (
                        monte_carlo.get_best_move_in_time(
                            self.board
                        )
                    )
                    played_move = True
                    player_type = "Minimax"
                    moves_calculated = (
                        monte_carlo.get_moves_calculated()
                    )

                if played_move:
                    other_colour_count = (
                        rules.get_number_of_white_pieces(
                            self.board.piece_matrix
                        )
                        if self.current_colour
                        == Colour.BLACK
                        else rules.get_number_of_black_pieces(
                            self.board.piece_matrix
                        )
                    )
                    self.board.place_piece_at_position(
                        self.current_colour,
                        position.position,
                    )

                    new_count = (
                        rules.get_number_of_white_pieces(
                            self.board.piece_matrix
                        )
                        if self.current_colour
                        == Colour.BLACK
                        else rules.get_number_of_black_pieces(
                            self.board.piece_matrix
                        )
                    )
                    if (
                        self.current_colour
                        == PlayerTurn.BLACK
                    ):
                        self.player1_captures += (
                            other_colour_count - new_count
                        )
                    else:
                        self.player2_captures += (
                            other_colour_count - new_count
                        )

                    self.current_colour = (
                        PlayerTurn.WHITE
                        if self.current_colour
                        is PlayerTurn.BLACK
                        else PlayerTurn.BLACK
                    )
                    database_move = DatabaseMove(
                        database_colour,
                        player_type,
                        moves_calculated,
                        self.board_size,
                        self.calculation_time,
                    )
                    insert_move(database_move)
            elif not self.sent_game_data:
                player1 = self.player1_text
                player2 = self.player2_text
                player1_territory = (
                    rules.get_black_territory(
                        self.board.piece_matrix
                    )
                )
                player1_captures = abs(
                    self.player1_captures
                )
                player2_territory = (
                    rules.get_white_territory(
                        self.board.piece_matrix
                    )
                )
                player2_captures = abs(
                    self.player2_captures
                )
                database_game = DatabaseGame(
                    player1,
                    player2,
                    self.board_size,
                    player1_territory,
                    player1_captures,
                    player2_captures,
                    player2_territory,
                    self.calculation_time,
                )
                insert_game(database_game)
                self.sent_game_data = True

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
                    or self.current_colour
                    is PlayerTurn.WHITE
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
            database_colour = (
                "Black"
                if self.current_colour == PlayerTurn.BLACK
                else "White"
            )
            database_move = DatabaseMove(
                database_colour,
                "Player",
                5,
                self.board_size,
                10,
            )
            insert_move(database_move)

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
        self.screen = pygame.display.set_mode(
            (width, height), RESIZABLE
        )

    def render(self):
        if self.game_running:
            self.board.render(self.screen)
            self.box.set_topleft((self.width - 225, 100))
            self.box.blit()
            self.box.update()
        elif not self.game_over:
            self.background.blit()
            self.main_menu_box.set_topleft(
                (self.width / 2 - 50, self.height / 2 - 50)
            )
            self.main_menu_box.blit()
            self.main_menu_box.update()

        pygame.display.flip()
