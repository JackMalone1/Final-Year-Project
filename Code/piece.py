from typing import Tuple

import pygame
from colours import Colour
from piece_display import *


class Piece:
    def __init__(self) -> None:
        self.position = tuple()

    def __init__(self, position: tuple()):
        self.position = position
        self.colour = Colour.CLEAR
        self.radius = 15

    def __init__(self, position: tuple(), colour: Colour, row: int, col: int):
        self.position = position
        self.colour = colour
        self.radius = 15
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.colour == other.colour

    def __hash__(self):
        return hash(('row', self.row, 'col', self.col, 'colour', self.colour))

    def render(self, surface: pygame.Surface):
        if self.colour != Colour.CLEAR:
            if self.colour is not Colour.CLEAR:
                if self.colour is Colour.BLACK:
                    image = black_piece_image
                elif self.colour is Colour.WHITE:
                    image = white_piece_image

                image_rect = image.get_rect()
                image_rect.x = self.position[0]
                image_rect.y = self.position[1]
                surface.blit(image, image_rect)

    def set_position(self, position: tuple):
        # can't modify tuple so convert to list to make the update and then we can convert back to a tuple
        position_list = list(self.position)
        position_list[0] = position[0] - 10
        position_list[1] = position[1] - 10
        self.position = tuple(position_list)

    def set_colour(self, colour: Colour):
        self.colour = colour

