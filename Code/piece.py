from typing import Tuple

import pygame
from colours import Colour
from piece_display import *


class Piece:
    """
    Representation of a piece on the board that contains the visual representation of it as well as the colour and position
    on the board for it
    """
    def __init__(self) -> None:
        self.position = tuple()

    def __init__(self, position: tuple()):
        self.position = position
        self.colour = Colour.CLEAR
        self.radius = 15

    def __init__(
        self,
        position: tuple(),
        colour: Colour,
        row: int,
        col: int,
    ):
        """
        Sets up the position and colour of the piece. Takes in a position and row and col. The position is for the visual
        representation and the row and col are for setting the position on the board
        :param position: position for the visual representation
        :param colour: colour for the piece
        :param row: row that the piece will be at
        :param col: column that the piece will be at
        """
        self.position = position
        self.colour = colour
        self.radius = 15
        self.row = row
        self.col = col

    def __eq__(self, other):
        return (
            self.row == other.row
            and self.col == other.col
            and self.colour == other.colour
        )

    def __hash__(self):
        return hash(
            (
                "row",
                self.row,
                "col",
                self.col,
                "colour",
                self.colour,
            )
        )

    def render(self, surface: pygame.Surface):
        """
        Renders the piece to the pygame surface that was passed in. Uses global images to render so that we don't need to
        make multiple copies of the same image which can impact performance
        :param surface: surface to render the piece to
        """
        if self.colour != Colour.CLEAR and self.colour != Colour.Ko:
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
        """
        Updates the visual representation of the piece
        :param position: position to set the piece to
        """
        # can't modify tuple so convert to list to make the update and then we can convert back to a tuple
        position_list = list(self.position)
        position_list[0] = position[0] - 10
        position_list[1] = position[1] - 10
        self.position = tuple(position_list)

    def set_colour(self, colour: Colour):
        """
        Updates the colour of the piece
        :param colour: colour to update the piece to
        """
        self.colour = colour
