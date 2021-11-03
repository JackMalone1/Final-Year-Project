from typing import Tuple
from colours import Colour

class piece:
    def __init__(self, position: Tuple(int, int)):
        self.position = position
        self.colour = Colour.CLEAR
        
    def init(self, position: Tuple(int, int), colour: Colour):
        self.position = position
        self.colour = colour