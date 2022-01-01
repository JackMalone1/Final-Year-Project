from board import Board
from colours import Colour
from playerturn import PlayerTurn
from copy import deepcopy, copy
import numpy as np


class Node:
    def __init__(self):
        self.parent = None
        self.score = 0
        self.visited = 0
        self.children = []
        self.total_simulations = 0
        self.won_simulations = 0

    def __init__(self, board: Board, player: PlayerTurn):
        self.__init__(self)
        self.parent = None
        self.possible_moves = []
        self.board = copy.deepcopy(board)
        self.player = player

    def __init__(self, parent, player: PlayerTurn, position: tuple):
        self.__init__(self)
        self.parent = parent
        self.player = player
        self.position = position
        self.board = copy.deepcopy(parent.board)
        self.current_colour = Colour.WHITE if player is PlayerTurn.WHITE else Colour.BLACK
        if self.board.piece_matrix[position[0]][position[1]].colour is Colour.CLEAR:
            self.board.piece_matrix[position[0]][position[1]].colour = self.current_colour

    def backup(self, evaluation):
        pass

    def expand_node(self):
        pass

    def get_best_child(self):
        pass

    # usual value for the exploration constant is sqrt(2)
    def uct1(self, exploration_param):
        return (self.won_simulation / self.total_simulations) + (exploration_param *
                                                                 np.sqrt(np.log(self.parent.total_simulations) /
                                                                         self.total_simulations))
