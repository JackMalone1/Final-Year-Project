import copy

from colours import Colour
from player_turn import player_turn
from piece import Piece


def remove_pieces(group: list):
    for piece in group:
        piece.colour = Colour.CLEAR


def is_koish(row: int, col: int, piece_matrix) -> Colour:
    piece = piece_matrix[row][col]
    if piece.colour is not Colour.CLEAR:
        return None
    colour = Colour.CLEAR
    if row - 1 > 0 and piece_matrix[row - 1][col].colour is not Colour.CLEAR:
        colour = piece_matrix[row - 1][col].colour
    if col - 1 > 0 and piece_matrix[row][col - 1].colour is not colour:
        return None
    if row + 1 < len(piece_matrix) and piece_matrix[row + 1][col].colour is not colour:
        return None
    if col + 1 < len(piece_matrix) and piece_matrix[row][col + 1].colour is not colour:
        return None
    return colour


class GoRules:
    def __init__(self, piece_matrix, size):
        self.size = size
        self.piece_matrix = piece_matrix
        self.current_colour = player_turn.BLACK

    def get_piece_at_position(self, row: int, col: int) -> Piece:
        return self.piece_matrix[row][col]

    def get_adjacent_of_colour(self, row: int, col: int, colour: Colour) -> list:
        adjacent_pieces = []
        if row - 1 >= 0 and self.get_piece_at_position(row - 1, col).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position(row - 1, col))
        if col - 1 >= 0 and self.get_piece_at_position(row, col - 1).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position(row, col - 1))
        if row + 1 <= self.size and self.get_piece_at_position(row + 1, col).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position(row + 1, col))
        if col + 1 <= self.size and self.get_piece_at_position(row, col + 1).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position(row, col + 1))
        return adjacent_pieces

    def is_move_legal(self, position: tuple, colour: Colour, current_colour: player_turn) -> bool:
        self.current_colour = current_colour
        if self.piece_matrix[position[0]][position[1]].colour is not Colour.CLEAR:
            return False
        liberties = self.get_adjacent_of_colour(position[0], position[1], Colour.CLEAR)
        surrounded_by_same_colour = self.get_adjacent_of_colour(position[0], position[1], colour)
        opposite_colour = Colour.BLACK if colour is Colour.WHITE else Colour.WHITE
        board_copy = copy.deepcopy(self.piece_matrix)
        board_copy[position[0]][position[1]].colour = colour
        self.remove_captured_groups_from_board(board_copy)
        can_be_placed = True if board_copy[position[0]][position[1]].colour is colour else False
        if not liberties and not surrounded_by_same_colour and not can_be_placed:
            return False
        if len(self.get_adjacent_of_colour(position[0], position[1], opposite_colour)) == 4 and not can_be_placed:
            return False
        return True

    def get_liberties_for_group(self, group: list) -> set:
        liberties = set()

        for piece in group:
            piece_liberties = self.get_adjacent_of_colour(piece.row, piece.col, Colour.CLEAR)
            [liberties.add(liberty) for liberty in piece_liberties]

        return liberties

    def create_group_from_piece(self, row: int, col: int, group: list, colour: Colour) -> list:
        if row > self.size or row < 0 or col < 0 or col > self.size:
            return list()
        if not group:
            group = [self.get_piece_at_position(row, col)]
        else:
            group.append(self.get_piece_at_position(row, col))
        adjacent_pieces = self.get_adjacent_of_colour(row, col, colour)
        for piece in adjacent_pieces:
            if piece not in group:
                self.create_group_from_piece(piece.row, piece.col, group, colour)
        return group

    def get_all_groups_on_board(self, piece_matrix):
        groups = [[]]
        has_been_checked = [[False for row in range(self.size)] for col in range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                if piece_matrix[row][col].colour is not Colour.CLEAR:
                    if has_been_checked[row][col] is False:
                        group = self.create_group_from_piece(row, col, [], piece_matrix[row][col].colour)
                        has_been_checked[row][col]
                        groups.append(group)
        return groups

    def get_liberties_for_group(self, group) -> list:
        all_liberties = []
        for piece in group:
            liberties = self.get_adjacent_of_colour(piece.row, piece.col, Colour.CLEAR)
            all_liberties.extend(liberties)
        return list(set(all_liberties))

    def get_legal_spots_to_play(self, piece_matrix):
        possible_moves = []
        free_spaces = [piece for piece in piece_matrix if piece.colour is Colour.CLEAR]
        for piece in free_spaces:
            if len(self.get_adjacent_of_colour(piece.row, piece.col, Colour.CLEAR)) > 0:
                possible_moves.append(tuple(piece.row, piece.col))
        return possible_moves

    def remove_captured_groups_from_board(self, piece_matrix):
        groups = self.get_all_groups_on_board(piece_matrix)
        for group in groups:
            if len(group) > 0:
                if self.current_colour is player_turn.BLACK and group[0].colour is not Colour.BLACK \
                        or self.current_colour is player_turn.WHITE and group[0].colour is not Colour.WHITE:
                    liberties = self.get_liberties_for_group(group)
                    if len(liberties) == 0:
                        remove_pieces(group)

        for group in groups:
            if len(group) > 0:
                if self.current_colour is player_turn.BLACK and group[0].colour is Colour.BLACK \
                        or self.current_colour is player_turn.WHITE and group[0].colour is Colour.WHITE:
                    liberties = self.get_liberties_for_group(group)
                    if len(liberties) == 0:
                        remove_pieces(group)
        return piece_matrix
