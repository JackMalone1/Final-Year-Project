from typing import Tuple

import pygame
from colours import Colour


class Piece:
    def __init__(self) -> None:
        pass

    def __init__(self, position: tuple()):
        self.position = position
        self.colour = Colour.CLEAR
        self.radius = 15
        self.image = pygame.image.load("piece-black.png")
        self.image_rect = self.image.get_rect()
        self.image_rect.x = -10
        self.image_rect.y = -10

    def __init__(self, position: tuple(), colour: Colour):
        self.position = position
        self.colour = colour
        self.radius = 15
        self.image = pygame.image.load("piece-black.png")
        self.image_rect = self.image.get_rect()
        if colour is not Colour.CLEAR:
            if colour is Colour.BLACK:
                self.image = pygame.image.load("piece-black.png")
            elif colour is Colour.WHITE:
                self.image = pygame.image.load("piece-white.png")
        self.image_rect.x = -30
        self.image_rect.y = -30

    def render(self, surface: pygame.Surface):
        surface.blit(self.image, self.image_rect)

    def set_position(self, position: tuple):
        self.image_rect.x = position[0] - 10
        self.image_rect.y = position[1] - 10

    def set_colour(self, colour: Colour):
        self.colour = colour
        if colour is not Colour.CLEAR:
            if colour is Colour.BLACK:
                self.image = pygame.image.load("piece-black.png")
            elif colour is Colour.WHITE:
                self.image = pygame.image.load("piece-white.png")
            pos = (self.image_rect.x, self.image_rect.y)
            self.image_rect = self.image.get_rect()
            self.image_rect.x = pos[0]
            self.image_rect.y = pos[1]
