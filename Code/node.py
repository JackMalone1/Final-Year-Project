from board import Board
from playerturn import PlayerTurn
from copy import deepcopy, copy
import numpy as np


class Node:
    def __init__(self, board: Board, player: PlayerTurn):
        self.parent = None
        self.score = 0
        self.children = []
        self.board = copy.deepcopy(board)
        self.player = player
        self.total_simulations = 0
        self.won_simulations = 0

    def backup(self, evaluation):
        pass

    # usual value for the exploration constant is sqrt(2)
    def uct1(self, exploration_param):
        return (self.won_simulation / self.total_simulations) + (exploration_param *
                                                                 np.sqrt(np.log(self.parent.total_simulations) /
                                                                         self.total_simulations))
