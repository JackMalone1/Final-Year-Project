import math
import sys
from random import choice

from board import Board
from colours import Colour
from playerturn import PlayerTurn
from copy import deepcopy, copy
import numpy as np


class Node:
    def __init__(self, parent, player: PlayerTurn, position: tuple, board: Board):
        self.parent = None
        self.score = 0
        self.visited = 0
        self.children = []
        self.total_simulations = 0
        self.won_simulations = 0
        self.position = (-1, -1)
        self.parent = parent
        self.player = player
        self.position = position
        self.possible_moves = []
        if self.parent is not None:
            self.board = copy(parent.board)
        else:
            self.board = board
        self.current_colour = Colour.WHITE if player is PlayerTurn.WHITE else Colour.BLACK
        #if self.board.piece_matrix[position[0]][position[1]].colour is Colour.CLEAR:
            #self.board.piece_matrix[position[0]][position[1]].colour = self.current_colour

    def backup(self, evaluation):
        self.score += evaluation
        self.visited += 1
        
        if self.parent is not None:
            self.parent.backup(evaluation)

    def expand_node(self):
        if len(self.possible_moves) > 0:
            node = choice(self.possible_moves)
            self.children.append(node)
            return node
        return None

    def get_more_moves(self, moves):
        [self.possible_moves.append(Node(self, Colour.WHITE, move, None)) for move in moves]

    def get_best_child(self):
        best_child = None
        best_value = -sys.maxsize
        for child in self.children:
            if child.uct1(math.sqrt(2)) > best_value:
                best_child = child
                best_value = child.uct1(math.sqrt(2))
        return best_child

    # usual value for the exploration constant is sqrt(2)
    def uct1(self, exploration_param):
        return (self.score / self.visited) + (exploration_param *
                                                                 np.sqrt(np.log(self.parent.visited) /
                                                                         self.visited))
