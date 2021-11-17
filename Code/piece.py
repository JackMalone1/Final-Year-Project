from typing import Tuple

import pygame
from colours import Colour
class piece:
    def __init__(self) -> None:
        pass
    def __init__(self, position: tuple()):
        self.position = position
        self.colour = Colour.CLEAR
        self.radius = 15
        
    def __init__(self, position: tuple(), colour: Colour):
        self.position = position
        self.colour = colour
        self.radius = 15

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.colour.value, self.position, self.radius)