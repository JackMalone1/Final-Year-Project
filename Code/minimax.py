from copy import copy, deepcopy
from datetime import datetime, timedelta
from board import Board
from colours import Colour
from database_zobrist import DatabaseZobrist
from go_rules import GoRules
from zobristDatabaseCRUD import get_zobrist_by_hash, insert_zobrist_hash
from zobrist_hashing import Zobrist


class Move:
    """
    Used to store the moves that the minimax function is currently looking at
    stores the depth of the move in case the algorithm has to finish early and you need to check the depth
    of each move so that only moves on the first depth are used for actually playing
    The score is the estimated evaluation for how good the state is. A positive score is good for black, negative score
    is good for white
    """
    position = ()
    score = 0
    depth = 0


class MiniMax:
    """
    Class that generates a move for a given board state using the Alpha Beta Minimax algorithm. Use the get best
    move
    in time function passing in the board state that you want to generate a move for for the class to generate a move.
    The algorithm has a time limit for how long it has to generate a move so the algorithm is likely to exit before it
    is able to fully search the game tree. This means that it wont have scores for some moves in the game so it will just
    pick the best score from the available moves that it has been able to calculate a score for.
    """
    def __init__(self, max_depth: int, size: int, zobrist: Zobrist, use_zobrist: bool):
        self.MAX_DEPTH = max_depth
        self.moves = []
        self.calculation_time = 1
        self.start_time = datetime.utcnow()
        self.size = size
        self.min_value = -100_000_000
        self.max_value = 100_000_000
        self.moves_calculated = 0
        self.zobrist = zobrist
        self.use_zobrist = use_zobrist

    def get_moves_calculated(self) -> int:
        """
        Gets how many moves that the algorithm was able to go through depending on how much time it was given as well as
        the size of the board that it was generating a move for.
        :return: the number of moves that were calculated
        """
        return self.moves_calculated

    def get_best_move_in_time(self, state, is_maximiser: bool) -> Move:
        """
        Generates a best move in the time given.
        :param board: State that we want to generate a move for
        :return: the move chosen for the state
        """
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
            return played_move
        else:
            return None

    def minimiser(
        self,
        state: Board,
        alpha: int,
        beta: int,
        depth: int,
    ) -> Move:
        """
        Picks a move for the minimiser, This will pick the next move with the lowest possible score. Looks through all
        of the possible next moves unless it is able to prune a branch. Will exit early if the time limit is reached so that
        these functions don't cause the algorithm to take longer than it was given.
        :param state: the current board state. This is a copy of the actual board so that moves are able to be played.
        :param alpha: best score found so far
        :param beta: lowest score so far
        :param depth: current depth that we are looking at. If at max depth will return evaluation for this move
        :return: the best move that it was able to find
        """
        rules = GoRules(state, self.size)
        possible_moves = rules.get_legal_spots_to_play(state)
        hash = self.zobrist.hash(state)
        states = get_zobrist_by_hash(hash)

        if len(states) > 0 and self.use_zobrist:
            leaf = Move()
            leaf.score = states[0][1]
            leaf.position = (0, 0)
            return leaf

        if (
            depth == self.MAX_DEPTH
            or len(possible_moves) == 0
            or self.is_time_limit_reached()
        ):
            leaf = Move()
            leaf.score = rules.score(state)
            leaf.position = (0, 0)
            if self.use_zobrist:
                zobrist_hash = DatabaseZobrist(hash, leaf.score)
                insert_zobrist_hash(zobrist_hash)
            return leaf

        move = Move()
        move.position = (0, 0)
        move.score = 0

        for possible_move in possible_moves:
            if depth == 0:
                self.moves_calculated += 1
            board_copy = deepcopy(state)
            board_copy[possible_move[0]][possible_move[1]].colour = Colour.WHITE
            if self.is_time_limit_reached():
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
        self,
        state: Board,
        alpha: int,
        beta: int,
        depth: int,
    ) -> Move:
        """
        Picks a move for the maximiser, This will pick the next move with the highest possible score. Looks through all
        of the possible next moves unless it is able to prune a branch. Will exit early if the time limit is reached so that
        these functions don't cause the algorithm to take longer than it was given.
        :param state: the current board state. This is a copy of the actual board so that moves are able to be played.
        :param alpha: best score found so far
        :param beta: lowest score so far
        :param depth: current depth that we are looking at. If at max depth will return evaluation for this move
        :return: the best move that it was able to find
        """
        rules = GoRules(state, self.size)
        possible_moves = rules.get_legal_spots_to_play(state)
        hash = self.zobrist.hash(state)
        states = get_zobrist_by_hash(hash)

        if len(states) > 0 and self.use_zobrist:
            leaf = Move()
            leaf.score = states[0][1]
            leaf.position = (0, 0)
            return leaf

        if (
            depth == self.MAX_DEPTH
            or len(possible_moves) == 0
            or self.is_time_limit_reached()
        ):
            leaf = Move()
            leaf.score = rules.score(state)
            leaf.position = (0, 0)
            if self.use_zobrist:
                zobrist_hash = DatabaseZobrist(hash, leaf.score)
                insert_zobrist_hash(zobrist_hash)
            return leaf

        move = Move()
        move.position = (0, 0)
        move.score = 0

        for possible_move in possible_moves:
            board_copy = deepcopy(state)
            board_copy[possible_move[0]][possible_move[1]].colour = Colour.BLACK
            if self.is_time_limit_reached():
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

    def is_time_limit_reached(self) -> bool:
        """
        checks if the algorithm has run out of time
        :return: returns true if it has used up all of the available time
        """
        current_time = datetime.utcnow()
        difference = current_time - self.start_time
        return difference >= timedelta(seconds=self.calculation_time)
