from board import Board
from player_turn import player_turn
from copy import deepcopy, copy


class Node:
    def __init__(self, board: Board, player: player_turn):
        self.parent = None
        self.score = 0
        self.children = []
        self.board = copy.deepcopy(board)
        self.player = player

    def backup(self, evaluation):
        pass
