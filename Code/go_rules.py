import copy

from colours import Colour
from player_turn import player_turn
from piece import Piece


def remove_pieces(group: list, piece_matrix):
    for piece in group:
        piece_matrix[piece.row][piece.col].colour = Colour.CLEAR


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
        self.number_of_opposite_captured = 0
        self.ko_position = (-1, -1)
        self.captured_groups = []

    def get_piece_at_position(self, row: int, col: int) -> Piece:
        return self.piece_matrix[row][col]

    def get_piece_at_position_on_board(self, row: int, col: int, piece_matrix) -> Piece:
        return piece_matrix[row][col]

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

    def get_adjacent_of_colour_on_board(self, row: int, col: int, colour: Colour, piece_matrix) -> list:
        adjacent_pieces = []
        if row - 1 >= 0 and self.get_piece_at_position_on_board(row - 1, col, piece_matrix).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position_on_board(row - 1, col, piece_matrix))
        if col - 1 >= 0 and self.get_piece_at_position_on_board(row, col - 1, piece_matrix).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position_on_board(row, col - 1, piece_matrix))
        if row + 1 <= self.size and self.get_piece_at_position_on_board(row + 1, col, piece_matrix).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position_on_board(row + 1, col, piece_matrix))
        if col + 1 <= self.size and self.get_piece_at_position_on_board(row, col + 1, piece_matrix).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position_on_board(row, col + 1, piece_matrix))
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
        self.number_of_opposite_captured = 0
        self.remove_captured_groups_from_board(board_copy, colour)
        can_be_placed = True if board_copy[position[0]][position[1]].colour is colour else False
        if not liberties and not surrounded_by_same_colour and not can_be_placed:
            return False
        print(len(self.get_adjacent_of_colour_on_board(position[0], position[1], opposite_colour, board_copy)))
        if len(self.get_adjacent_of_colour_on_board(position[0], position[1], opposite_colour, board_copy)) == 4 and \
                can_be_placed is False:
            return False

        if len(self.create_group_from_piece(position[0], position[1], [], colour)) == 1:
            if self.number_of_opposite_captured == 1:
                return False
        #possible_ko_colour = is_koish(position[0], position[1], self.piece_matrix)
        #if len(self.captured_groups) > 0:
            #captured_piece_position = (self.captured_groups[0].row, self.captured_groups[0].col)
            #if position == self.ko_position:
                #print("Positions match")
                #return False
           # if self.number_of_opposite_captured == 1 and possible_ko_colour == opposite_colour:
                # self.ko_position = (self.captured_groups[0].row, self.captured_groups[0].col)
                #self.ko_position = captured_piece_position
                #print("ko position, row: ", self.ko_position[0], " col: ", self.ko_position[1])
                #print("position, row: ", position[0], " col: ", position[1])

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

    def remove_captured_groups_from_board(self, piece_matrix, colour):
        groups = self.get_all_groups_on_board(piece_matrix)
        opposite_colour = Colour.BLACK if colour is Colour.WHITE else Colour.WHITE
        for group in groups:
            if len(group) > 0:
                if self.current_colour is player_turn.BLACK and group[0].colour is not Colour.BLACK \
                        or self.current_colour is player_turn.WHITE and group[0].colour is not Colour.WHITE:
                    liberties = self.get_liberties_for_group(group)
                    if len(liberties) == 0:
                        self.number_of_opposite_captured += 1
                        remove_pieces(group, piece_matrix)

        for group in groups:
            if len(group) > 0:
                if self.current_colour is player_turn.BLACK and group[0].colour is Colour.BLACK \
                        or self.current_colour is player_turn.WHITE and group[0].colour is Colour.WHITE:
                    liberties = self.get_liberties_for_group(group)
                    if len(liberties) == 0:
                        remove_pieces(group, piece_matrix)
        return piece_matrix
