import math
from copy import copy
from datetime import datetime
from random import choice, random

from board import Board
from colours import Colour
from go_rules import GoRules
from node import Node
from playerturn import PlayerTurn


class MonteCarloTreeSearch:
    def __init__(self, board: Board, colour: Colour):
        self.calculation_time = 10
        self.board = board
        self.states = []
        self.max_moves = 10
        self.colour = colour

    def get_best_move_in_time(self):
        start_time = datetime.utcnow()
        rules = GoRules(self.board.piece_matrix, self.board.size)
        available_moves = rules.get_legal_spots_to_play(self.board)
        root = None
        best_value = -math.inf
        best_move = available_moves[0]
        moves = []
        if len(available_moves) > 0:
            root = Node(self.board.copy())
            if root is not None:
                for _ in range(10):
                    n = self.expand(root)
                    n.backup(self.run_simulation(n))
                    difference = datetime.utcnow() - start_time
                    if difference.total_seconds() < self.calculation_time:
                        break  # we've used all of our time so find whatever the best move was and return
                for node in n.children:
                    if node.visited == 0:
                        continue
                    ucb = node.uct1(math.sqrt(2))
                    if ucb > best_value:
                        best_move = node
                        best_value = ucb
                moves.append((0, best_move.position))
                self.board.piece_matrix[moves[0][0], moves[0][1]] = self.colour

    def expansion(self, node: Node):
        n = copy(node)
        rules = GoRules()
        moves = rules.get_legal_spots_to_play(n.board.piece_matrix)

        while len(moves) > 0:
            n.get_more_moves(rules.get_legal_spots_to_play(n.board.piece_matrix))
            if len(n.possible_moves) > 0:
                return n.expand_node()
            else:
                n = n.get_best_child()
        return n

    def run_simulation(self, node: Node):
        states_copy = node.board.copy()
        rules = GoRules()

        while len(rules.get_legal_spots_to_play(states_copy.piece_matrix)) > 0:
            possible_moves = rules.get_legal_spots_to_play(states_copy.piece_matrix)
            move = choice(possible_moves)

            if states_copy.current_player == PlayerTurn.BLACK:
                states_copy.piece_matrix[move[0]][move[1]] = Colour.BLACK
                states_copy.current_player = PlayerTurn.WHITE
            else:
                states_copy.piece_matrix[move[0]][move[1]] = Colour.WHITE
                states_copy.current_player = PlayerTurn.BLACK
        if states_copy.get_number_of_black_pieces() > states_copy.get_number_of_white_pieces():
            return 1
        elif states_copy.get_number_of_white_pieces() > states_copy.get_number_of_black_pieces():
            return -1
        else:
            return 0
