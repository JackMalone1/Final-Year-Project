import string
from typing import Tuple
from piece import Piece
import pygame
from pygame import freetype
from colours import Colour
from playerturn import PlayerTurn
from string import ascii_uppercase
import copy
from go_rules import *
from go_rules import GoRules


class Text:
    """
    A string that has a position attached to make it easier to be displayed in the window.
    """
    def __init__(self, text: str, position: tuple):
        self.string = text
        self.position = position


class Board:
    """
    This class holds the visual representation of the board. This includes the background and naming of all of the different
    positions of the board and pieces after they are placed. Also stores where all of the actual pieces are placed on the board.
    Also includes ko so that pieces cannot be placed at that positions.
    """
    def __init__(
        self,
        background: pygame.image,
        size: int,
        font_path: string,
        piece_sound_effect_path,
    ):
        """

        :param background: Sprite representing the background
        :param size: Size of the board that you want to be created
        :param font_path: Font to be used for the naming of the different positions
        :param piece_sound_effect_path: Sound effect for when you place a piece as a player
        """
        self.has_ko = False
        self.size = size - 1
        self.font = freetype.Font(font_path, 24)
        self.numbers = ["" for i in range(self.size + 1)]
        self.letters = ["" for x in range(self.size + 1)]
        self.board = [[0 for x in range(self.size)] for y in range(self.size)]
        self.board_intersections = [
            [0 for x in range(self.size + 1)] for y in range(self.size + 1)
        ]
        self.background = background
        self.background_rect = background.get_rect()
        w, h = (800, 800)
        self.tile_size = (w / self.size) * 0.9
        self.offset = 30
        self.set_up_grid()
        self.piece_matrix = [
            [Piece((-10, -10), Colour.CLEAR, row, col) for col in range(self.size + 1)]
            for row in range(self.size + 1)
        ]
        self.play_piece_sound = pygame.mixer.Sound(piece_sound_effect_path)
        self.current_colour = PlayerTurn.BLACK
        self.rules = GoRules(self.piece_matrix, self.size)

    def render(self, screen: pygame.display) -> None:
        """
        Renders all of the board data to the screen
        :param screen: Pygame display that you want to display the board to
        """
        screen.blit(self.background, self.background_rect)
        [
            [pygame.draw.rect(screen, pygame.Color(0, 0, 0), col, 3) for col in row]
            for row in self.board
        ]

        for row in self.piece_matrix:
            for piece in row:
                piece.render(screen)
        [
            self.font.render_to(
                screen,
                number.position,
                number.string,
                (0, 0, 0),
            )
            for number in self.numbers
        ]
        [
            self.font.render_to(
                screen,
                letter.position,
                letter.string,
                (0, 0, 0),
            )
            for letter in self.letters
        ]

    def check_mouse_position(self, mouse_position, current_colour: PlayerTurn) -> bool:
        """
        Takes in the current mouse position and checks if it intersects any of the possible position and uses pygame
        rectangles so that there is some extra space where they are able to place a piece. Also takes in the current colour
        so that it is able to place that piece
        :param mouse_position: position of the mouse as a tuple
        :param current_colour: what colour piece should be placed if the piece is able to be placed
        :return: whether or not a piece was placed
        """
        for x in range(self.size + 1):
            for y in range(self.size + 1):
                if self.board_intersections[x][y].collidepoint(mouse_position):
                    if self.piece_matrix[x][y].colour is Colour.CLEAR:
                        self.play_piece_sound.play()
                        return self.place_piece_at_position(current_colour, (x, y))
        return False

    def place_ko(self, rules, colour, position):
        """
        After a piece is captured and ko has occured, this will place ko at the correct position so that for the next move
        it is not possible to play at this position.
        :param rules: rules class so that it is able to figure out where to place ko
        :param colour: colour of piece to place that captured to create the ko state
        :param position: position of the new piece to place
        """
        row, col = (
            rules.killed_groups[0][0].row,
            rules.killed_groups[0][0].col,
        )
        self.piece_matrix[row][col].set_colour(Colour.Ko)
        self.piece_matrix[position[0]][position[1]].set_position(
            self.board_intersections[position[0]][position[1]].center
        )
        self.piece_matrix[position[0]][position[1]].set_colour(colour)

    def remove_ko(self, colour, position):
        """
        Call after the move that ko was placed. This will remove the status of ko and let players to place at this position
        again
        :param colour: colour of piece that you want to place
        :param position: position of the piece that you want to place
        """
        self.piece_matrix[position[0]][position[1]].set_position(
            self.board_intersections[position[0]][position[1]].center
        )
        self.piece_matrix[position[0]][position[1]].set_colour(colour)

        for row in self.piece_matrix:
            for piece in row:
                if piece.colour is Colour.Ko:
                    piece.colour = Colour.CLEAR

    def place_piece_at_position(
        self, current_colour: PlayerTurn, position: tuple
    ) -> bool:
        """
        takes in a position and colour for a piece to be placed. Then checks if the move is legal to play and if it is then
        it will place the piece and remove any captured pieces from the board. Will also return whether or not the piece
        was placed so that the current player can be switched.
        :param current_colour: colour of the piece to be placed
        :param position: position to place the piece at
        :return: whether or not the piece was actually placed.
        """
        has_placed_piece = False
        rules = GoRules(self.piece_matrix, self.size)
        if current_colour is PlayerTurn.BLACK and rules.is_move_legal(
            position, Colour.BLACK, current_colour
        ):
            if rules.possible_ko:
                has_placed_piece = True
                self.place_ko(rules, Colour.BLACK, position)
            else:
                has_placed_piece = True
                self.remove_ko(Colour.BLACK, position)
        elif current_colour is PlayerTurn.WHITE and rules.is_move_legal(
            position, Colour.WHITE, current_colour
        ):
            if rules.possible_ko:
                has_placed_piece = True
                self.place_ko(rules, Colour.WHITE, position)
            else:
                has_placed_piece = True
                self.remove_ko(Colour.WHITE, position)
        if has_placed_piece:
            rules = GoRules(self.piece_matrix, self.size)
            rules.opposite_colour = (
                Colour.BLACK if current_colour is PlayerTurn.WHITE else Colour.WHITE
            )
            self.piece_matrix = rules.remove_captured_groups_from_board(
                self.piece_matrix
            )
        return has_placed_piece

    def set_up_numbers(self) -> None:
        """
        Creates all of the text in the correct position to display at the side of the board so that all of the positions are
        labelled correctly. Places the letters along the y axis and the numbers along the x axis.
        """
        starting_position = (
            self.board_intersections[-1][-1].x,
            self.board_intersections[-1][-1].y,
        )
        x = self.board[0][0].x
        y = starting_position[1] + 25
        letters = list(ascii_uppercase)
        letters = [
            letter for letter in letters if "I" not in letter
        ]  # I does not show up on the board so remove
        # from list
        for i in range(self.size + 1):
            x = self.offset + (i * self.tile_size)
            self.letters[i] = Text(text=letters[i], position=(x, y))

        x = self.board[0][0].x - 25
        y = self.board[0][0].y
        number = 19
        for i in range(self.size + 1):
            y = self.offset + (i * self.tile_size)
            self.numbers[i] = Text(text=str(number), position=(x, y))
            number -= 1

    def set_up_grid(self) -> None:
        """
        Sets up all of the collisions for the board so that an actual player can place a piece on the board as these
        collisions are used to check where the player clicks on the board.
        """
        for y in range(self.size + 1):
            y_position = self.offset + (y * self.tile_size)
            for x in range(self.size + 1):
                if x < self.size and y < self.size:
                    x_position = self.offset + (x * self.tile_size)
                    rect = pygame.Rect(
                        x_position,
                        y_position,
                        self.tile_size,
                        self.tile_size,
                    )
                    intersection = pygame.Rect(
                        x_position - 5,
                        y_position - 5,
                        10,
                        10,
                    )
                    self.board[x][y] = rect
                    self.board_intersections[x][y] = intersection
                else:
                    x_position = self.offset + (x * self.tile_size)
                    intersection = pygame.Rect(
                        x_position - 5,
                        y_position - 5,
                        10,
                        10,
                    )
                    self.board_intersections[x][y] = intersection
        self.set_up_numbers()

    def get_piece_at_position(self, row: int, col: int) -> Piece:
        """
        Returns a piece at a given position
        :param row: row of the piece
        :param col: column of the piece
        :return: the piece at that position
        """
        return self.piece_matrix[row][col]

    def get_number_of_black_pieces(self) -> int:
        """
        Goes through the entire board and counts how many black pieces there are
        :return: the number of black pieces that are on the board
        """
        sum = 0
        for row in self.piece_matrix:
            for piece in row:
                if piece.colour == Colour.BLACK:
                    sum += 1
        return sum

    def get_number_of_white_pieces(self) -> int:
        """
        Goes through the entire board and counts how many white pieces there are
        :return: the number of white pieces that are on the board
        """
        sum = 0
        for row in self.piece_matrix:
            for piece in row:
                if piece.colour == Colour.WHITE:
                    sum += 1
        return sum
