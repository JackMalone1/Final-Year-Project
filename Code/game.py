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
import uuid

from zobrist_hashing import Zobrist


def react_func(event):
    """
    Test function for the UI
    """
    print("Hello")


class GameManager:
    def __init__(self):
        """
        Used as the main game class that includes the main game loop that handles input, updates and rendering
        This will handle running both the Alpha Beta and Minimax algorithms as well as handling whenever the player places
        something on the board
        """
        self.sent_game_data = False
        self.player1_text = ""
        self.player2_text = ""
        self.player1_captures = 0
        self.player2_captures = 0
        self.move_number = 0
        self.game_id = uuid.uuid1()
        self.init()
        self.init_ui()
        self.calculation_time = 5

    def init_pygame_and_display(self):
        """
        Initialises pygame and sets up a basic window with a title
        """
        pygame.init()
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Monte Carlo Tree Search")
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height), RESIZABLE)

    def init_board(self):
        """
        sets up the initial board with the background image and a default size
        This will be overwritten once the game is started with the correct size of the board
        """
        background = pygame.image.load("Assets//background.jpg")
        self.board_size = 5
        self.board = Board(
            background=background,
            size=self.board_size,
            font_path="MONOFONT.ttf",
            piece_sound_effect_path="Assets//Sounds//place_piece.ogg",
        )

    def init_variables(self):
        """
        initialises the basic game variables
        """
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_colour = PlayerTurn.BLACK
        self.time_delta = 0
        self.has_passed = False
        self.game_running = False
        self.game_over = False

    def init(self):
        """
        runs all of the other init functions to make sure that everything is set up in the game correctly
        """
        self.init_pygame_and_display()
        self.init_board()
        self.init_variables()

    def pass_func(self):
        """
        checks if both of the players passed in a row, if they did then the game is over
        """
        if self.has_passed:
            self.game_running = False
            self.game_over = True
        self.has_passed = True
        if self.current_colour is PlayerTurn.BLACK:
            self.current_colour = PlayerTurn.WHITE
        elif self.current_colour is PlayerTurn.WHITE:
            self.current_colour = PlayerTurn.BLACK

    def select_player_one(self):
        """
        Check which one of the radio buttons was selected on the main menu once the player chooses to start the game and
        then uses this to set up if the first player should either be an actual player, the Monte Carlo algorithm or
        the Alpha Beta algorithm
        """
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

    def select_player_two(self):
        """
        Check which one of the radio buttons was selected on the main menu once the player chooses to start the game and
        then uses this to set up if the second player should either be an actual player, the Monte Carlo algorithm or
        the Alpha Beta algorithm
        """
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

    def select_time_allocated(self):
        """
        Check which one of the radio buttons was selected on the main menu once the player chooses to start the game and
        then uses this to set up how long both of the algorithms are allowed per move
        Once the time limit is reached the algorithms will return the best move that they have found so far if they were
        not able to fully finish the algorithm
        """
        time_allocated = self.time_radio_pool.get_selected()
        if time_allocated == self.five_seconds_button:
            self.calculation_time = 5
        elif time_allocated == self.fifteen_seconds_button:
            self.calculation_time = 15
        elif time_allocated == self.twenty_seconds_button:
            self.calculation_time = 20

    def select_board_size(self):
        """
        Check which one of the radio buttons was selected on the main menu once the player chooses to start the game and
        then uses this to set up what board size the game should use. All of the boards are squares, so choosing 5 will return
        a 5x5 board to play on
        """
        board_size = self.board_size_pool.get_selected()
        if board_size == self.five_by_five_board:
            self.create_board(5)
            self.board_size = 5
        elif board_size == self.nine_by_nine_board:
            self.create_board(9)
            self.board_size = 9
        elif board_size == self.thirteen_by_thirteen_board:
            self.create_board(13)
            self.board_size = 13
        elif board_size == self.nineteen_by_nineteen_board:
            self.create_board(19)
            self.board_size = 19
        self.zobrist = Zobrist(self.board_size)

    def start_game(self):
        """
        sets up the players for both black and white
        makes sure to use the correct ai or actual player for both players based on what radio button was pressed
        """
        self.game_running = True
        self.select_player_one()
        self.select_player_two()
        self.select_time_allocated()
        self.select_board_size()

    def create_board(self, size):
        """
        creates the board class with the correct size based on what was picked inside of the main menu
        """
        self.board_size = size
        background = pygame.image.load("Assets//background.jpg")
        self.board = Board(
            background=background,
            size=self.board_size,
            font_path="MONOFONT.ttf",
            piece_sound_effect_path="Assets//Sounds//place_piece.ogg",
        )

    def init_buttons_and_boxes(self):
        """
        Creates all of the buttons that will be displayed on the main menu of the game
        """
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
        self.player2_button = thorpy.Checker("Player", type_="radio")
        self.monte_carlo2_button = thorpy.Checker("Monte Carlo", type_="radio")
        self.alpha_beta2_button = thorpy.Checker("Alpha Beta", type_="radio")
        self.five_seconds_button = thorpy.Checker("5", type_="radio")
        self.fifteen_seconds_button = thorpy.Checker("15", type_="radio")
        self.twenty_seconds_button = thorpy.Checker("20", type_="radio")
        self.five_by_five_board = thorpy.Checker("5x5", type_="radio")
        self.nine_by_nine_board = thorpy.Checker("9x9", type_="radio")
        self.thirteen_by_thirteen_board = thorpy.Checker("13x13", type_="radio")
        self.nineteen_by_nineteen_board = thorpy.Checker("19x19", type_="radio")
        self.text = thorpy.Element(text="Player 1")
        self.player2 = thorpy.Element(text="Player 2")
        self.time_limit = thorpy.Element(text="Time Limit")
        self.board_size_text = thorpy.Element(text="Board Size")

    def init_ui_variables(self):
        """
        Sets up the variables that will be set by the radio buttons on the main menu
        """
        self.player_player1 = False
        self.monte_carlo_player1 = False
        self.alpha_beta_player1 = False
        self.player_player2 = False
        self.monte_carlo_player2 = False
        self.alpha_beta_player2 = False

    def init_radio_pools(self):
        """
        Groups all of the radio buttons based on if they are being used to set up either of the players, the board size or
        the amount of time per move
        """
        self.radio_pool = thorpy.RadioPool(
            [
                self.player_button,
                self.monte_carlo_button,
                self.alpha_beta_button,
            ],
            first_value=self.player_button,
        )

        self.player2_radio_pool = thorpy.RadioPool(
            [
                self.player2_button,
                self.monte_carlo2_button,
                self.alpha_beta2_button,
            ],
            first_value=self.player2_button,
        )

        self.time_radio_pool = thorpy.RadioPool(
            [
                self.five_seconds_button,
                self.fifteen_seconds_button,
                self.twenty_seconds_button,
            ],
            first_value=self.five_seconds_button,
        )

        self.board_size_pool = thorpy.RadioPool(
            [
                self.five_by_five_board,
                self.nine_by_nine_board,
                self.thirteen_by_thirteen_board,
                self.nineteen_by_nineteen_board,
            ],
            first_value=self.five_by_five_board,
        )

    def init_ui_display(self):
        """
        Places all of the buttons in their correct position as well as setting up the background for the main menu
        """
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
        self.main_menu = thorpy.Menu(elements=self.background, fps=60)

    def init_ui(self):
        """
        Creates all of the different UI buttons for the main menu screen. This lets you start the game
        as well as deciding what ai you want to play against or play against someone else or wathc the ai play.
        """
        self.init_buttons_and_boxes()
        self.init_ui_variables()
        self.init_radio_pools()
        self.init_ui_display()

    def run(self):
        """
        game loop for the game
        processes events as well as rendering the game
        """
        while self.running:
            self.time_delta = self.clock.tick(60) / 1000.0
            self.update()
            self.process_events()
            self.render()

    def send_game_data(self):
        """
        sends the results of a game to the database so that the jupyter notebook is able to process this data
        uses the database CRUD file to interface with the sqlite database so we don't need any specific code in here
        """
        rules = GoRules(self.board.piece_matrix, self.board.size)
        player1 = self.player1_text
        player2 = self.player2_text
        player1_territory = rules.get_black_territory(self.board.piece_matrix)
        player1_captures = abs(self.player1_captures)
        player2_territory = rules.get_white_territory(self.board.piece_matrix)
        player2_captures = abs(self.player2_captures)
        database_game = DatabaseGame(
            player1,
            player2,
            self.board_size,
            player1_territory,
            player1_captures,
            player2_captures,
            player2_territory,
            self.calculation_time,
            str(self.game_id),
        )
        insert_game(database_game)
        self.sent_game_data = True

    def is_maximiser(self) -> bool:
        """
        This is used for the Alpha Beta algorithm to know if it should take the min or the max score that it has found at a
        specific depth of the game.
        Since black plays first in the game I decided to pick black as the maximiser
        """
        return True if self.current_colour is PlayerTurn.BLACK else False

    def get_current_colour(self) -> Colour:
        """
        Gets the Colour of the current player. This changes the Player turn Black into Colour Black
        """
        return Colour.BLACK if self.current_colour == PlayerTurn.BLACK else Colour.WHITE

    def get_current_colour_as_string(self):
        """
        Gets string representation of the current colour. This is used to send the data of the current move to the database
        as we can't store custom datatypes
        """
        return "Black" if self.current_colour == PlayerTurn.BLACK else "White"

    def switch_turns(self):
        """
        Called after the current player successfully places a piece somewhere on the board to change who's turn it is
        """
        return (
            PlayerTurn.WHITE
            if self.current_colour is PlayerTurn.BLACK
            else PlayerTurn.BLACK
        )

    def get_count_of_opposite_colour(self):
        """
        Gets the number of the opponents pieces on the board. This is used to keep track of the number of captures for each player
        player as it is calculated before and after each move on the board so that at the end of the game we know who had the
        most captures in the game
        """
        rules = GoRules(self.board.piece_matrix, self.board.size)
        return (
            rules.get_number_of_white_pieces(self.board.piece_matrix)
            if self.current_colour == Colour.BLACK
            else rules.get_number_of_black_pieces(self.board.piece_matrix)
        )

    def update(self):
        """
        runs the code for both the alpha beta algorithm and the minimax algorithm as well as sending data to the
        database
        :return:
        """
        if self.game_running:
            rules = GoRules(self.board.piece_matrix, self.board.size)
            moves = rules.get_legal_spots_to_play(self.board.piece_matrix)
            colour = self.get_current_colour()

            database_colour = self.get_current_colour_as_string()
            player_type = ""
            moves_calculated = 0

            if len(moves) > 0:
                monte_carlo = MonteCarloTreeSearch(self.board, colour)
                monte_carlo.calculation_time = self.calculation_time
                alpha_beta = MiniMax(4, self.board.size, self.zobrist, False)
                alpha_beta.calculation_time = self.calculation_time

                is_maximiser = self.is_maximiser()
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
                    player_type = "AlphaBeta"
                    moves_calculated = alpha_beta.get_moves_calculated()
                elif (
                    self.current_colour is PlayerTurn.BLACK and self.monte_carlo_player1
                ) or (
                    self.current_colour is PlayerTurn.WHITE and self.monte_carlo_player2
                ):
                    position = monte_carlo.get_best_move_in_time(self.board)
                    played_move = True
                    player_type = "MonteCarlo"
                    moves_calculated = monte_carlo.get_moves_calculated()

                if played_move:
                    self.move_number += 1
                    other_colour_count = self.get_count_of_opposite_colour()

                    self.board.place_piece_at_position(
                        self.current_colour,
                        position.position,
                    )

                    new_count = self.get_count_of_opposite_colour()

                    if self.current_colour == PlayerTurn.BLACK:
                        self.player1_captures += other_colour_count - new_count
                    else:
                        self.player2_captures += other_colour_count - new_count

                    self.current_colour = self.switch_turns()
                    database_move = DatabaseMove(
                        database_colour,
                        player_type,
                        moves_calculated,
                        self.board_size,
                        self.calculation_time,
                        self.move_number,
                        str(self.game_id),
                    )
                    insert_move(database_move)
            elif not self.sent_game_data:
                self.send_game_data()

    def is_actual_player_turn(self):
        """
        Checks if the current player is an actual player
        :return: returns true if an actual player, false otherwise
        """
        return (
            self.current_colour is PlayerTurn.BLACK
            and self.player_player1
            or self.current_colour is PlayerTurn.WHITE
            and self.player_player2
        )

    def process_events(self):
        """
        goes through all mouse and keyboard events and responds to them accordingly
        also sends the events to the ui library so that it is able to update the ui on the screen
        """
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
                if self.is_actual_player_turn():
                    self.place_piece()
            if self.game_running:
                self.menu.react(event)
            elif not self.game_over:
                self.main_menu.react(event)

    def place_piece(self):
        """
        Checks if it is possible to place a piece and if it is then it is placed
        """
        placed_piece = self.board.check_mouse_position(
            pygame.mouse.get_pos(), self.current_colour
        )
        if placed_piece:
            self.has_passed = False
            database_colour = self.get_current_colour_as_string()
            self.move_number += 1
            database_move = DatabaseMove(
                database_colour,
                "Player",
                5,
                self.board_size,
                10,
                self.move_number,
                str(self.game_id),
            )
            insert_move(database_move)

            self.current_colour = self.switch_turns()

    def resize_window(self, event):
        """
        Resizes the window based on the input from the player, set a minimum width and height so that the game is still
        visible even if they try to make it to small
        :param event: event from the player
        """
        width, height = event.size
        if width < self.width:
            width = self.width
        if height < self.height:
            height = self.height
        self.screen = pygame.display.set_mode((width, height), RESIZABLE)

    def render(self):
        """
        Renders either the game or the main menu depending on what state that the game is in
        """
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
