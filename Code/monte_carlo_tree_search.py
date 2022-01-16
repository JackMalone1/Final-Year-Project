import math
from copy import copy, deepcopy
from datetime import datetime
from random import choice, random

from board import Board
from colours import Colour
from go_rules import GoRules
from node import Node
from playerturn import PlayerTurn


class MonteCarloTreeSearch:
    def __init__(self, board: Board, colour: Colour):
        self.calculation_time = 1
        self.board = board
        self.board.piece_matrix = deepcopy(board.piece_matrix)
        self.states = []
        self.max_moves = 10
        self.colour = colour
        self.player_turn = PlayerTurn.WHITE if self.colour == Colour.WHITE else PlayerTurn.BLACK
        self.start_time = datetime.utcnow()

    def get_best_move_in_time(self, board):
        #self.start_time = datetime.utcnow()
        rules = GoRules(self.board.piece_matrix, self.board.size)
        available_moves = rules.get_legal_spots_to_play(self.board.piece_matrix)
        root = None
        best_value = -math.inf
        if available_moves is None or len(available_moves) == 0:
            return
        best_move = available_moves[0]
        moves = []
        if len(available_moves) > 0:
            root = Node(None, self.player_turn, (-1, -1), copy(self.board))
            self.player_turn = PlayerTurn.WHITE if self.colour == Colour.WHITE else PlayerTurn.BLACK
            if root is not None:
                for _ in range(10):
                    n = self.expansion(root)
                    n.backup(self.run_simulation(n))
                    difference = datetime.utcnow() - self.start_time
                    if difference.total_seconds() < self.calculation_time:
                        break  # we've used all of our time so find whatever the best move was and return
                for node in n.children:
                    if node.visited == 0:
                        continue
                    ucb = node.uct1(math.sqrt(2))
                    if ucb > best_value:
                        best_move = node
                        best_value = ucb
                moves.append((0, best_move))
                move = moves[0][1]
                board.place_piece_at_position(self.player_turn, move)

    def expansion(self, node: Node):
        n = copy(node)
        rules = GoRules(n.board.piece_matrix, n.board.size)
        moves = rules.get_legal_spots_to_play(n.board.piece_matrix)

        while len(moves) > 0:
            n.get_more_moves(rules.get_legal_spots_to_play(n.board.piece_matrix))
            if len(n.possible_moves) > 0:
                return n.expand_node()
            else:
                n = n.get_best_child()
        return n

    def run_simulation(self, node: Node):
        states_copy = copy(node.board)
        rules = GoRules(states_copy.piece_matrix, states_copy.size)
        difference = datetime.utcnow() - self.start_time
        while len(rules.get_legal_spots_to_play(states_copy.piece_matrix)) > 0 and difference.total_seconds() < self.calculation_time:
            possible_moves = rules.get_legal_spots_to_play(states_copy.piece_matrix)
            move = choice(possible_moves)

            if states_copy.current_colour == PlayerTurn.BLACK:
                states_copy.place_piece_at_position(PlayerTurn.BLACK, move)
                #board_copy[move[0]][move[1]].colour = Colour.BLACK
                states_copy.current_colour = PlayerTurn.WHITE
            else:
                states_copy.place_piece_at_position(PlayerTurn.WHITE, move)
                #board_copy[move[0]][move[1]].colour = Colour.WHITE
                states_copy.current_colour = PlayerTurn.BLACK
            difference = datetime.utcnow() - self.start_time
        if rules.get_number_of_black_pieces(states_copy.piece_matrix) > rules.get_number_of_white_pieces(states_copy.piece_matrix):
            return 1
        elif rules.get_number_of_white_pieces(states_copy.piece_matrix) > rules.get_number_of_black_pieces(states_copy.piece_matrix):
            return -1
        else:
            return 0
