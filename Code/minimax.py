from copy import copy, deepcopy
from datetime import datetime, timedelta
from board import Board
from colours import Colour
from go_rules import GoRules


class Move:
    position = ()
    score = 0
    depth = 0


class MiniMax:
    def __init__(self, max_depth: int, size: int):
        self.MAX_DEPTH = max_depth
        self.moves = []
        self.calculation_time = 1
        self.start_time = datetime.utcnow()
        self.size = size
        self.min_value = -100_000_000
        self.max_value = 100_000_000

    def get_best_move_in_time(self, state, is_maximiser: bool) -> Move:
        self.start_time = datetime.utcnow()
        rules = GoRules(copy(state), self.size)
        possible_moves = rules.get_legal_spots_to_play(copy(state))

        if len(possible_moves) > 0:
            played_move = Move()
            played_move.position = (0, 0)

            if is_maximiser:
                played_move.position = self.maximiser(
                    state, self.min_value, self.max_value, 0
                ).position
            else:
                played_move.position = self.minimiser(
                    state, self.min_value, self.max_value, 0
                ).position
            print("finished")
            return played_move
        else:
            return None

    def minimiser(
        self, state: Board, alpha: int, beta: int, depth: int
    ) -> Move:
        rules = GoRules(state, self.size)
        possible_moves = rules.get_legal_spots_to_play(state)
        if depth == self.MAX_DEPTH or len(possible_moves) == 0:
            leaf = Move()
            leaf.score = rules.score(state)
            leaf.position = (0, 0)
            if leaf.score != 0:
                print("Non 0 score: " + str(leaf.score))
            return leaf

        move = Move()
        move.position = (0, 0)
        move.score = 0

        for possible_move in possible_moves:
            board_copy = deepcopy(state)
            board_copy[possible_move[0]][possible_move[1]].colour = Colour.WHITE
            if self.is_time_limit_reached():
                print("Time limit reached")
                possible_score = rules.score(board_copy)
                if possible_score <= alpha:
                    move.score = possible_score
                    move.position = possible_move
                    return move
                return move
            score = self.maximiser(board_copy, alpha, beta, depth + 1).score
            if score <= alpha:
                move.score = alpha
                move.position = possible_move
                return move
            if score < beta:
                beta = score
                move.position = possible_move
        move.score = beta
        return move

    def maximiser(
        self, state: Board, alpha: int, beta: int, depth: int
    ) -> Move:
        rules = GoRules(state, self.size)
        possible_moves = rules.get_legal_spots_to_play(state)
        if depth == self.MAX_DEPTH or len(possible_moves) == 0:
            leaf = Move()
            leaf.score = rules.score(state)
            leaf.position = (0, 0)
            if leaf.score != 0:
                print("Non 0 score: " + str(leaf.score))
            return leaf

        move = Move()
        move.position = (0, 0)
        move.score = 0

        for possible_move in possible_moves:
            board_copy = deepcopy(state)
            board_copy[possible_move[0]][possible_move[1]].colour = Colour.BLACK
            if self.is_time_limit_reached():
                print("Time limit reached")
                possible_score = rules.score(board_copy)
                if possible_score >= beta:
                    move.score = possible_score
                    move.position = possible_move
                    return move
                return move
            score = self.minimiser(board_copy, alpha, beta, depth + 1).score
            if score >= beta:
                move.score = beta
                move.position = possible_move
                return move
            if score > alpha:
                alpha = score
                move.position = possible_move

        move.score = alpha
        return move

    def is_time_limit_reached(self):
        current_time = datetime.utcnow()
        difference = current_time - self.start_time
        return difference >= timedelta(seconds=30)

