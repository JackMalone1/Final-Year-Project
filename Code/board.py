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
    def __init__(self, text: str, position: tuple):
        self.string = text
        self.position = position


class Board:
    def __init__(
        self,
        background: pygame.image,
        size: int,
        font_path: string,
        piece_sound_effect_path,
    ):
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
            [
                Piece((-10, -10), Colour.CLEAR, row, col)
                for col in range(self.size + 1)
            ]
            for row in range(self.size + 1)
        ]
        self.play_piece_sound = pygame.mixer.Sound(piece_sound_effect_path)
        self.current_colour = PlayerTurn.BLACK
        self.rules = GoRules(self.piece_matrix, self.size)

    def render(self, screen: pygame.display) -> None:
        screen.blit(self.background, self.background_rect)
        [
            [
                pygame.draw.rect(screen, pygame.Color(0, 0, 0), col, 3)
                for col in row
            ]
            for row in self.board
        ]

        for row in self.piece_matrix:
            for piece in row:
                piece.render(screen)
        [
            self.font.render_to(
                screen, number.position, number.string, (0, 0, 0)
            )
            for number in self.numbers
        ]
        [
            self.font.render_to(
                screen, letter.position, letter.string, (0, 0, 0)
            )
            for letter in self.letters
        ]

    def check_mouse_position(
        self, mouse_position, current_colour: PlayerTurn
    ) -> bool:
        for x in range(self.size + 1):
            for y in range(self.size + 1):
                if self.board_intersections[x][y].collidepoint(mouse_position):
                    if self.piece_matrix[x][y].colour is Colour.CLEAR:
                        self.play_piece_sound.play()
                        return self.place_piece_at_position(
                            current_colour, (x, y)
                        )
        return False

    def place_ko(self, rules, colour, position):
        row, col = rules.killed_groups[0][0].row, rules.killed_groups[0][0].col
        self.piece_matrix[row][col].set_colour(Colour.Ko)
        self.piece_matrix[position[0]][position[1]].set_position(
            self.board_intersections[position[0]][position[1]].center
        )
        self.piece_matrix[position[0]][position[1]].set_colour(colour)

    def remove_ko(self, colour, position):
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
                Colour.BLACK
                if current_colour is PlayerTurn.WHITE
                else Colour.WHITE
            )
            self.piece_matrix = rules.remove_captured_groups_from_board(
                self.piece_matrix
            )
        return has_placed_piece

    def set_up_numbers(self) -> None:
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
        for y in range(self.size + 1):
            y_position = self.offset + (y * self.tile_size)
            for x in range(self.size + 1):
                if x < self.size and y < self.size:
                    x_position = self.offset + (x * self.tile_size)
                    rect = pygame.Rect(
                        x_position, y_position, self.tile_size, self.tile_size
                    )
                    intersection = pygame.Rect(
                        x_position - 5, y_position - 5, 10, 10
                    )
                    self.board[x][y] = rect
                    self.board_intersections[x][y] = intersection
                else:
                    x_position = self.offset + (x * self.tile_size)
                    intersection = pygame.Rect(
                        x_position - 5, y_position - 5, 10, 10
                    )
                    self.board_intersections[x][y] = intersection
        self.set_up_numbers()

    def get_piece_at_position(self, row: int, col: int) -> Piece:
        return self.piece_matrix[row][col]

    def get_number_of_black_pieces(self):
        sum = 0
        for row in self.piece_matrix:
            for piece in row:
                if piece.colour == Colour.BLACK:
                    sum += 1
        return sum

    def get_number_of_white_pieces(self):
        sum = 0
        for row in self.piece_matrix:
            for piece in row:
                if piece.colour == Colour.WHITE:
                    sum += 1
        return sum
