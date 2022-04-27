import math
import sys
from random import choice, random, randrange

from board import Board
from colours import Colour
from playerturn import PlayerTurn
from copy import deepcopy, copy
import numpy as np


class Node:
    """
    A node inside of the monte carlo tree search algorithm. Stores the score, parent and children of the node as well as
    an indication of how good the move is.
    """
    def __init__(
        self,
        parent,
        player: PlayerTurn,
        position: tuple,
        board: Board,
    ):
        """
        Sets up the Node with a parent and a player and position with the board state. For a root node the parent can be
        marked as None
        :param parent: The parent of the node
        :param player: The player that this node is related to
        :param position: The position that the move is being played at
        :param board: The current board state
        """
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
            self.board = parent.board
        else:
            self.board = board
        self.current_colour = (
            Colour.WHITE if player is PlayerTurn.WHITE else Colour.BLACK
        )
        # if self.board.piece_matrix[position[0]][position[1]].colour is Colour.CLEAR:
        # self.board.piece_matrix[position[0]][position[1]].colour = self.current_colour

    def backup(self, evaluation):
        """
        Increases the score of the node by the evaluation and then propagates this score backup to their parent if they have one.
        Also increases their visited count so that the monte carlo algorithm nows how many times this node has been looked at.
        :param evaluation: how much to increase the score by
        """
        self.score += evaluation
        self.visited += 1

        if self.parent is not None:
            self.parent.backup(evaluation)

    def expand_node(self):
        """
        Create an additional child nodes for this node from the possible moves from this position
        :return: the created child node
        """
        if len(self.possible_moves) > 0:
            index = randrange(0, len(self.possible_moves))
            node = self.possible_moves[index]
            self.possible_moves.pop(index)
            self.children.append(node)
            return node
        return None

    def get_more_moves(self, moves):
        """
        Adds more possible moves based on the moves given
        :param moves: the moves that you want to add
        """
        [
            self.possible_moves.append(Node(self, Colour.WHITE, move, None))
            for move in moves
        ]

    def get_best_child(self):
        """
        looks through all of the child nodes for the node and finds the one with the best score
        :return: the child that has the best uct1 value
        """
        best_child = None
        best_value = -sys.maxsize
        for child in self.children:
            if child.uct1(math.sqrt(2)) > best_value:
                best_child = child
                best_value = child.uct1(math.sqrt(2))
        return best_child

    # usual value for the exploration constant is sqrt(2)
    def uct1(self, exploration_param):
        """
        Implements the uct1 algorithm
        :param exploration_param: the exploration parameter to be used. Usually should be around sqrt(2)
        :return: the uct1 value for this node
        """
        return (self.score / self.visited) + (
            exploration_param * np.sqrt(np.log(self.parent.visited) / self.visited)
        )

    def as_copy(self, other_node):
        """
        Copies over the values from the other node into this node
        :param other_node: node that you want to copy over
        """
        self.score = other_node.score
        self.visited = other_node.visited
        self.parent = other_node.parent
        self.children = deepcopy(other_node.children)
        self.possible_moves = deepcopy(other_node.possible_moves)
        self.position = other_node.position
