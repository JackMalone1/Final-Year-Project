import copy

from colours import Colour
from playerturn import PlayerTurn
from piece import Piece


def remove_pieces(group: list):
    for piece in group:
        piece.colour = Colour.CLEAR


def is_koish(row: int, col: int, piece_matrix) -> set:
    colours = list()
    if row - 1 > 0:
        colours.append(
            int(piece_matrix[row - 1][col].colour)
        )
    if col - 1 > 0:
        colours.append(
            int(piece_matrix[row][col - 1].colour)
        )
    if row + 1 < len(piece_matrix):
        colours.append(
            int(piece_matrix[row + 1][col].colour)
        )
    if col + 1 < len(piece_matrix):
        colours.append(
            int(piece_matrix[row][col + 1].colour)
        )
    return colours


class GoRules:
    def __init__(self, piece_matrix, size):
        self.size = size
        self.piece_matrix = piece_matrix
        self.current_colour = PlayerTurn.BLACK
        self.possible_ko = False
        self.ko_position = None
        self.killed_groups = []

    def get_piece_at_position(
        self, row: int, col: int
    ) -> Piece:
        return self.piece_matrix[row][col]

    def get_adjacent_of_colour(
        self, row: int, col: int, colour: Colour
    ) -> list:
        adjacent_pieces = []
        if (
            row - 1 >= 0
            and self.get_piece_at_position(
                row - 1, col
            ).colour
            is colour
        ):
            adjacent_pieces.append(
                self.get_piece_at_position(row - 1, col)
            )
        if (
            col - 1 >= 0
            and self.get_piece_at_position(
                row, col - 1
            ).colour
            is colour
        ):
            adjacent_pieces.append(
                self.get_piece_at_position(row, col - 1)
            )
        if (
            row + 1 <= self.size
            and self.get_piece_at_position(
                row + 1, col
            ).colour
            is colour
        ):
            adjacent_pieces.append(
                self.get_piece_at_position(row + 1, col)
            )
        if (
            col + 1 <= self.size
            and self.get_piece_at_position(
                row, col + 1
            ).colour
            is colour
        ):
            adjacent_pieces.append(
                self.get_piece_at_position(row, col + 1)
            )
        return adjacent_pieces

    def is_move_legal(
        self,
        position: tuple,
        colour: Colour,
        current_colour: PlayerTurn,
    ) -> bool:
        self.current_colour = current_colour
        if (
            self.piece_matrix[position[0]][
                position[1]
            ].colour
            is not Colour.CLEAR
        ):
            return False
        self.opposite_colour = (
            Colour.BLACK
            if colour is Colour.WHITE
            else Colour.WHITE
        )

        board_copy = self.piece_matrix.copy()

        for i in range(len(self.piece_matrix)):
            for j in range(len(self.piece_matrix)):
                board_copy[i][j].colour = self.piece_matrix[
                    i
                ][j].colour
        board_copy[position[0]][position[1]].colour = colour
        self.remove_captured_groups_from_board(board_copy)
        liberties = self.get_adjacent_of_colour(
            position[0], position[1], Colour.CLEAR
        )
        liberties.extend(
            self.get_adjacent_of_colour(
                position[0], position[1], Colour.Ko
            )
        )
        surrounded_by_same_colour = self.get_adjacent_of_colour(
            position[0], position[1], colour
        )
        can_be_placed = (
            True
            if board_copy[position[0]][position[1]].colour
            is colour
            else False
        )
        if (
            not liberties
            and not surrounded_by_same_colour
            and not can_be_placed
        ):
            return False
        if (
            len(
                self.get_adjacent_of_colour(
                    position[0],
                    position[1],
                    self.opposite_colour,
                )
            )
            == 4
            and not can_be_placed
        ):
            return False
        # print(self.killed_groups)
        self.possible_ko = False
        if (
            len(self.killed_groups) == 1
            and len(self.killed_groups[0]) == 1
        ):
            # print(self.opposite_colour)
            # print(self.killed_groups[0][0].colour)
            self.possible_ko = True
            self.ko_position = (
                self.killed_groups[0][0].row,
                self.killed_groups[0][0].col,
            )
            return True

        return True

    def get_liberties_for_group(self, group: list) -> set:
        liberties = set()

        for piece in group:
            piece_liberties = self.get_adjacent_of_colour(
                piece.row, piece.col, Colour.CLEAR
            )
            [
                liberties.add(liberty)
                for liberty in piece_liberties
            ]

        return liberties

    def create_group_from_piece(
        self,
        row: int,
        col: int,
        group: list,
        colour: Colour,
    ) -> list:
        if (
            row > self.size
            or row < 0
            or col < 0
            or col > self.size
        ):
            return list()
        if not group:
            group = [self.get_piece_at_position(row, col)]
        else:
            group.append(
                self.get_piece_at_position(row, col)
            )
        adjacent_pieces = self.get_adjacent_of_colour(
            row, col, colour
        )
        for piece in adjacent_pieces:
            if piece not in group:
                self.create_group_from_piece(
                    piece.row, piece.col, group, colour
                )
        return group

    def get_all_groups_on_board(self, piece_matrix):
        groups = [[]]
        has_been_checked = [
            [False for row in range(self.size + 1)]
            for col in range(self.size + 1)
        ]

        for row in range(self.size + 1):
            for col in range(self.size + 1):
                if (
                    piece_matrix[row][col].colour
                    != Colour.CLEAR
                ):
                    if not has_been_checked[row][col]:
                        group = self.create_group_from_piece(
                            row,
                            col,
                            [],
                            piece_matrix[row][col].colour,
                        )
                        has_been_checked[row][col] = True
                        groups.append(group)
        return groups

    def get_liberties_for_group(self, group) -> list:
        all_liberties = []
        for piece in group:
            liberties = self.get_adjacent_of_colour(
                piece.row, piece.col, Colour.CLEAR
            )
            all_liberties.extend(liberties)
            all_liberties.extend(
                self.get_adjacent_of_colour(
                    piece.row, piece.col, Colour.Ko
                )
            )
        return list(set(all_liberties))

    def get_legal_spots_to_play(self, piece_matrix):
        possible_moves = []
        free_spaces = []

        for row in piece_matrix:
            for piece in row:
                if piece.colour is Colour.CLEAR:
                    free_spaces.append(piece)
        for piece in free_spaces:
            if (
                len(
                    self.get_adjacent_of_colour(
                        piece.row, piece.col, Colour.CLEAR
                    )
                )
                > 0
            ):
                possible_moves.append(
                    (piece.row, piece.col)
                )
        return possible_moves

    def next_state(self, piece_matrix, position):
        piece_matrix[position[0]][
            position[1]
        ].colour = Colour.BLACK
        return piece_matrix

    def remove_captured_groups_from_board(
        self, piece_matrix
    ):
        groups = self.get_all_groups_on_board(piece_matrix)
        groups = [group for group in groups if group != []]
        for group in groups:
            if len(group) > 0:
                if group[0].colour == self.opposite_colour:
                    if group[0].colour != Colour.Ko:
                        liberties = self.get_liberties_for_group(
                            group
                        )
                        if len(liberties) == 0:
                            self.killed_groups.append(
                                copy.deepcopy(group)
                            )
                            remove_pieces(group)

        for group in groups:
            if len(group) > 0:
                if (
                    group[0].colour != self.opposite_colour
                    and group[0].colour != Colour.CLEAR
                ):
                    if group[0].colour != Colour.Ko:
                        liberties = self.get_liberties_for_group(
                            group
                        )
                        if len(liberties) == 0:
                            self.killed_groups.append(
                                copy.deepcopy(group)
                            )
                            remove_pieces(group)
        return piece_matrix

    def get_next_board_state(self, board_state, move):
        pass

    def winner(self, state_history):
        # if the game is won, return which player won the game, otherwise return if it's still being played or
        # return if it is a tie
        pass

    def get_number_of_black_pieces(self, piece_matrix):
        sum = 0
        for row in piece_matrix:
            for piece in row:
                if piece.colour == Colour.BLACK:
                    sum += 1
        return sum

    def get_number_of_white_pieces(self, piece_matrix):
        sum = 0
        for row in piece_matrix:
            for piece in row:
                if piece.colour == Colour.WHITE:
                    sum += 1
        return sum

    """
    Defining black territory as any empty spot that is fully surrounded by only black
    """

    def get_black_territory(self, piece_matrix):
        sum = 0
        for row in range(len(piece_matrix)):
            for col in range(len(piece_matrix[row])):
                if piece_matrix[row][
                    col
                ].colour == Colour.CLEAR and len(
                    self.get_adjacent_of_colour(
                        row, col, Colour.BLACK
                    )
                ):
                    sum += 1
        return sum

    """
    Defining white territory as any empty spot that is fully surrounded by only white
    """

    def get_white_territory(self, piece_matrix):
        sum = 0
        for row in range(len(piece_matrix)):
            for col in range(len(piece_matrix[row])):
                if piece_matrix[row][
                    col
                ].colour == Colour.CLEAR and len(
                    self.get_adjacent_of_colour(
                        row, col, Colour.WHITE
                    )
                ):
                    sum += 1
        return sum

    """
    returns an integer representation of how the game is approximately going
    black will have a positive when they are winning and will return a negative value if white is winning
    if 0 is returned then the game is fairly simple
    the function is kept fairly simple as it will be called a lot inside of the minimax algorithm so needs to be
    as fast as possible
    """

    def score(self, piece_matrix):
        return (
            self.get_number_of_black_pieces(piece_matrix)
            + self.get_black_territory(piece_matrix)
            - self.get_number_of_white_pieces(piece_matrix)
            - self.get_white_territory(piece_matrix)
        )

    def get_territory_for_black(self, piece_matrix):
        sum = 0
        for row in piece_matrix:
            for piece in row:
                if piece.colour == Colour.CLEAR:
                    liberties = self.get_adjacent_of_colour(
                        piece.row, piece.col, Colour.BLACK
                    )
                    if len(liberties) > 2:
                        sum += 1
        return sum

    def get_territory_for_white(self, piece_matrix):
        sum = 0
        for row in piece_matrix:
            for piece in row:
                if piece.colour == Colour.CLEAR:
                    liberties = self.get_adjacent_of_colour(
                        piece.row, piece.col, Colour.WHITE
                    )
                    if len(liberties) > 2:
                        sum += 1
        return sum
