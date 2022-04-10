import random

from colours import Colour
from go_rules import GoRules


class Zobrist:
    def __init__(self, size: int):
        self.size = size
        self.table = [[0] * 3 for i in range(size*size)]
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                random_bits = random.getrandbits(128)
                print(random_bits)
                self.table[i][j] = random_bits

    def hash(self, state):
        row = 0
        col = 0
        h = 0
        for i in range(len(self.table)):
            col += 1
            row += 1
            if row >= self.size:
                row = 0
                col = 0
            rules = GoRules(state, self.size)
            if not rules.get_piece_at_position(row, col).colour == Colour.CLEAR:
                colour = rules.get_piece_at_position(row, col).colour
                if colour == Colour.BLACK:
                    colour = 1
                elif colour == Colour.WHITE:
                    colour = 2
                elif colour == Colour.Ko:
                    colour = 3
                j = colour
                h ^= self.table[i][j]
        return h

