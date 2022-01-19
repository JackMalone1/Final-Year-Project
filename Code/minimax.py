from datetime import datetime

from board import Board
from go_rules import *


class Move:
    position = ()
    score = 0
    depth = 0


class MiniMax:
    def __init__(self, max_depth: int):
        self.MAX_DEPTH = max_depth
        self.moves = []
        self.calculation_time = 1
        self.start_time = datetime.utcnow()

    def do_move_in_time(self, alpha, beta, state: Board, depth, move, is_minimiser, player_colour) -> Move:
        if depth == self.MAX_DEPTH:
            return self.evaluate(state, move, depth)
        rules = GoRules(state.piece_matrix, state.size)
        available_moves = rules.get_legal_spots_to_play(state.piece_matrix)
        for move in available_moves:
            difference = datetime.utcnow() - self.start_time
            if difference.total_seconds() < self.calculation_time:
                break  # we've used all of our time so find whatever the best move was and return
            possible_move = Move()
            if not is_minimiser:
                opposite_colour = Colour.BLACK if player_colour == Colour.WHITE else Colour.WHITE
                state.place_piece_at_position(opposite_colour, move)
                new_depth = depth + 1
                result = self.do_move_in_time(alpha, beta, state, new_depth, move, not is_minimiser, opposite_colour)
                score = result.score
                alpha = max(alpha, score)
                if alpha >= beta:
                    possible_move.score = alpha
                    possible_move.depth = depth
                    self.moves.append(possible_move)
                    state.place_piece_at_position(Colour.CLEAR, move)
                    return move
                move.score = score
            else:
                opposite_colour = Colour.BLACK if player_colour == Colour.WHITE else Colour.WHITE
                state.place_piece_at_position(opposite_colour, move)
                new_depth = depth + 1
                score = self.do_move_in_time(alpha, beta, state, new_depth, move, not is_minimiser,
                                             opposite_colour).score
                beta = min(beta, score)

                if alpha >= beta:
                    possible_move.score = beta
                    possible_move.depth = depth
                    self.moves.append(possible_move)
                    state.place_piece_at_position(Colour.CLEAR, move)
                    return possible_move
                possible_move.score = score
            possible_move.depth = depth
            self.moves.append(possible_move)
            state.place_piece_at_position(Colour.CLEAR, move)
        best_move = self.moves[0]
        best_depth = self.MAX_DEPTH + 1

        if is_minimiser:
            best_score = 10000000
            for m in self.moves:
                if m.score < best_score and m.depth <= best_depth:
                    best_move = m
                    best_score = m.score
                    best_depth = m.depth
        else:
            best_score = -10000000
            for m in self.moves:
                if m.score > best_score and m.depth <= best_depth:
                    best_move = m
                    best_score = m.score
                    best_depth = m.depth
        return best_move

    def evaluate(self, state, move, depth):
        evaluated_move = Move()
        evaluated_move.depth = depth
        evaluated_move.position = move
        evaluated_move.score = 1
        return evaluated_move
