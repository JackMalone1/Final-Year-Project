from typing import Tuple
from piece import Piece
import pygame
from pygame import freetype
from colours import Colour
from player_turn import player_turn
from string import ascii_uppercase


class Text:
    def __init__(self, string: str, position: tuple):
        self.string = string
        self.position = position


class Board:
    def __init__(self, background: pygame.image, size: int):
        self.size = size - 1
        self.font = freetype.Font("MONOFONT.ttf", 24)
        self.numbers = ['' for i in range(self.size + 1)]
        self.letters = ['' for x in range(self.size + 1)]
        self.board = [[0 for x in range(self.size)] for y in range(self.size)]
        self.board_intersections = [[0 for x in range(self.size + 1)] for y in range(self.size + 1)]
        self.background = background
        self.background_rect = background.get_rect()
        w, h = pygame.display.get_surface().get_size()
        self.tile_size = (w / self.size) * 0.9
        self.offset = 30
        self.set_up_grid()
        self.piece_matrix = [[Piece((-10, -10), Colour.CLEAR) for x in range(self.size + 1)] for y in
                             range(self.size + 1)]
        self.play_piece_sound = pygame.mixer.Sound('Assets/Sounds/place_piece.ogg')

    def render(self, screen: pygame.display) -> None:
        screen.blit(self.background, self.background_rect)
        [[pygame.draw.rect(screen, pygame.Color(0, 0, 0), col, 3) for col in row] for row in self.board]

        for row in self.piece_matrix:
            for piece in row:
                piece.render(screen)
        [self.font.render_to(screen, number.position, number.string, (0, 0, 0)) for number in self.numbers]
        [self.font.render_to(screen, letter.position, letter.string, (0, 0, 0)) for letter in self.letters]

    def check_mouse_position(self, mouse_position, current_colour: player_turn) -> bool:
        for x in range(self.size + 1):
            for y in range(self.size + 1):
                if self.board_intersections[x][y].collidepoint(mouse_position):
                    print("Collision")
                    self.play_piece_sound.play()
                    self.piece_matrix[x][y].set_position(self.board_intersections[x][y].center)
                    if current_colour is player_turn.BLACK:
                        self.piece_matrix[x][y].set_colour(Colour.BLACK)
                    elif current_colour is player_turn.WHITE:
                        self.piece_matrix[x][y].set_colour(Colour.WHITE)
                    return True
        return False

    def set_up_numbers(self):
        starting_position = (self.board_intersections[-1][-1].x, self.board_intersections[-1][-1].y)
        x = self.board[0][0].x
        y = starting_position[1] + 10
        letters = list(ascii_uppercase)
        letters = [letter for letter in letters if 'I' not in letter]  # I does not show up on the board so remove
        # from list
        for i in range(self.size + 1):
            x = self.offset + (i * self.tile_size)
            self.letters[i] = Text(string=letters[i], position=(x, y))

        x = self.board[0][0].x - 20
        y = self.board[0][0].y
        number = 19
        for i in range(self.size + 1):
            y = self.offset + (i * self.tile_size)
            self.numbers[i] = Text(string=str(number), position=(x, y))
            number -= 1

    def set_up_grid(self):
        for y in range(self.size + 1):
            y_position = self.offset + (y * self.tile_size)
            for x in range(self.size + 1):
                if x < self.size and y < self.size:
                    x_position = self.offset + (x * self.tile_size)
                    rect = pygame.Rect(x_position, y_position, self.tile_size, self.tile_size)
                    intersection = pygame.Rect(x_position - 5, y_position - 5, 10, 10)
                    self.board[x][y] = rect
                    self.board_intersections[x][y] = intersection
                else:
                    x_position = self.offset + (x * self.tile_size)
                    intersection = pygame.Rect(x_position - 5, y_position - 5, 10, 10)
                    self.board_intersections[x][y] = intersection
        self.set_up_numbers()
