import copy

from colours import Colour
from playerturn import PlayerTurn
from piece import Piece


def remove_pieces(group: list):
    """
    sets all of the pieces in the group to clear so that they are no longer on the board
    :param group: group that you want to remove from the board
    """
    for piece in group:
        piece.colour = Colour.CLEAR


def is_koish(row: int, col: int, piece_matrix) -> set:
    colours = list()
    if row - 1 > 0:
        colours.append(int(piece_matrix[row - 1][col].colour))
    if col - 1 > 0:
        colours.append(int(piece_matrix[row][col - 1].colour))
    if row + 1 < len(piece_matrix):
        colours.append(int(piece_matrix[row + 1][col].colour))
    if col + 1 < len(piece_matrix):
        colours.append(int(piece_matrix[row][col + 1].colour))
    return colours


class GoRules:
    """
    This is a class that is used to check for different rules in the game such as checking if a move is legal that can be
    used to check if the move that an ai or player did is able to be done on the board. Is also used for capturing any
    groups on the board that has no liberties left as well as evaluating a board position depending on the territory for
    each colour which is used by the ai to make decisions on what moves to pick
    """

    def __init__(self, piece_matrix, size):
        """
        Sets up the rules for a certain state as well as size of board
        :param piece_matrix: state that we want to create a rules class for
        :param size: how big the board is for this state
        """
        self.size = size
        self.piece_matrix = piece_matrix
        self.current_colour = PlayerTurn.BLACK
        self.possible_ko = False
        self.ko_position = None
        self.killed_groups = []

    def get_piece_at_position(self, row: int, col: int) -> Piece:
        """
        Returns the piece at the given row and col. This may be an empty position and in that case the Piece returned
        will have a colour of either Clear or Ko
        :param row: row that we want to check
        :param col: col that we want to check
        :return: the Piece at that position
        """
        return self.piece_matrix[row][col]

    def get_adjacent_of_colour(self, row: int, col: int, colour: Colour) -> list:
        """
        Finds all of the adjacent pieces of the same colour for a specific piece on the board
        :param row: row of the piece to be checked
        :param col: col of the piece to be checked
        :param colour: colour of the piece to be checked
        :return: a list of all the pieces beside this piece that are the same colour. Returns an empty list if there is no
        piece of the same colour beside it
        """
        adjacent_pieces = []
        if row - 1 >= 0 and self.get_piece_at_position(row - 1, col).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position(row - 1, col))
        if col - 1 >= 0 and self.get_piece_at_position(row, col - 1).colour is colour:
            adjacent_pieces.append(self.get_piece_at_position(row, col - 1))
        if (
            row + 1 <= self.size
            and self.get_piece_at_position(row + 1, col).colour is colour
        ):
            adjacent_pieces.append(self.get_piece_at_position(row + 1, col))
        if (
            col + 1 <= self.size
            and self.get_piece_at_position(row, col + 1).colour is colour
        ):
            adjacent_pieces.append(self.get_piece_at_position(row, col + 1))
        return adjacent_pieces

    def is_move_legal(
        self,
        position: tuple,
        colour: Colour,
        current_colour: PlayerTurn,
    ) -> bool:
        """
        Takes in a position for a possible move to be played along with the colour of the piece that will be placed.
        First creates a copy of the board so that it is able to check if the board is legal without having to update the
        actual board position. It will then check if position has any liberties or if it is surrounded by pieces of the same
        colour. If it is then it is a valid move. If not will remove any dead groups from the board and then checks to see
        if the piece is still on the board to check if the piece placement was a valid capture or not. Also checks for Ko
        to make sure that positions can not be repeated infinitely on the board
        :param position: Position of where the piece will be placed
        :param colour: Colour of the piece to be placed
        :param current_colour: Whose turn it currently is
        :return: True if the piece is legal, otherwise False
        """
        self.current_colour = current_colour
        if self.piece_matrix[position[0]][position[1]].colour is not Colour.CLEAR:
            return False
        self.opposite_colour = Colour.BLACK if colour is Colour.WHITE else Colour.WHITE

        board_copy = self.piece_matrix.copy()

        for i in range(len(self.piece_matrix)):
            for j in range(len(self.piece_matrix)):
                board_copy[i][j].colour = self.piece_matrix[i][j].colour
        board_copy[position[0]][position[1]].colour = colour
        self.remove_captured_groups_from_board(board_copy)
        liberties = self.get_adjacent_of_colour(position[0], position[1], Colour.CLEAR)
        liberties.extend(
            self.get_adjacent_of_colour(position[0], position[1], Colour.Ko)
        )
        surrounded_by_same_colour = self.get_adjacent_of_colour(
            position[0], position[1], colour
        )
        can_be_placed = (
            True if board_copy[position[0]][position[1]].colour is colour else False
        )
        if not liberties and not surrounded_by_same_colour and not can_be_placed:
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

        self.possible_ko = False
        if len(self.killed_groups) == 1 and len(self.killed_groups[0]) == 1:
            self.possible_ko = True
            self.ko_position = (
                self.killed_groups[0][0].row,
                self.killed_groups[0][0].col,
            )
            return True

        return True

    def get_liberties_for_group(self, group: list) -> set:
        """
        Takes in a group and gets all of the liberties for this group. This is stored as a set so that pieces that are
        beside each other and share the same liberty do not duplicate this liberty so that we don't end up getting extra
        liberties for this group
        :param group: group that we want to get all of the liberties for
        :return: A set representing all of the liberties for the group. Will return a set of length 0 if the group has
        no liberties
        """
        liberties = set()

        for piece in group:
            piece_liberties = self.get_adjacent_of_colour(
                piece.row, piece.col, Colour.CLEAR
            )
            [liberties.add(liberty) for liberty in piece_liberties]

        return liberties

    def create_group_from_piece(
        self,
        row: int,
        col: int,
        group: list,
        colour: Colour,
    ) -> list:
        """
        takes in a particular piece along with its colour so that a group is able to be created for the piece with all
        of the other pieces surrounding it that are of the same colour. A piece has to be connected either
        horizontally or vertically to be added to the same group as another piece. This function is recursively called
        so that if there are several pieces in a row or that connect horizontally and vertically these pieces will still
        be added to the same group of pieces.
        :param row: row of the piece that you are checking
        :param col: col of the piece that you are checking
        :param group: current group that you have found for this piece
        :param colour: colour of piece that you are adding to this group. You only want to add pieces of the same colour
        to the group
        :return: A list representing all of the pieces in the group
        """
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

    def get_all_groups_on_board(self, piece_matrix) -> list:
        """
        Gets all of the groups on the board and then returns all of these groups as a list of lists. Uses another list
        of bools to keep track of what spots on the board it has already checked so that pieces and groups are not
        returned more than once from the function. Uses a helper function to create all of the groups once it finds
        either a black or white piece on the board. Does not create groups for empty spots or Ko.
        :param piece_matrix: The state that you want to get all of the groups for
        :return: A list of all of the groups which are another list of all of the Pieces in the group
        """
        groups = [[]]
        has_been_checked = [
            [False for row in range(self.size + 1)] for col in range(self.size + 1)
        ]

        for row in range(self.size + 1):
            for col in range(self.size + 1):
                if piece_matrix[row][col].colour != Colour.CLEAR:
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
        """
        Takes in a group and finds all adjacent spots that don't have any pieces on them as well as any spots with ko
        and adds these to the list of their liberties.
        Also momentarily changes these to a set before changing it back to a list so that the function does not
        count liberties more than once.
        :param group: the group that you want to get all of the liberties for.
        :return: A list of all the liberties for this group. Will return a group of length of 0 if they have no
        liberties.
        """
        all_liberties = []
        for piece in group:
            liberties = self.get_adjacent_of_colour(piece.row, piece.col, Colour.CLEAR)
            all_liberties.extend(liberties)
            all_liberties.extend(
                self.get_adjacent_of_colour(piece.row, piece.col, Colour.Ko)
            )
        return list(set(all_liberties))

    def get_legal_spots_to_play(self, piece_matrix) -> list:
        """
        goes through the state given and finds all spots that are able to be played at. It is possible to play at a
        position if there is no pieces already there, there isn't Ko at the spot and there is at least one liberty for
        that position
        :param piece_matrix: state that you want to get all possible moves for
        :return: returns a list of all possible positions to play at for this position
        """
        possible_moves = []
        free_spaces = []

        for row in piece_matrix:
            for piece in row:
                if piece.colour is Colour.CLEAR:
                    free_spaces.append(piece)
        for piece in free_spaces:
            if len(self.get_adjacent_of_colour(piece.row, piece.col, Colour.CLEAR)) > 0:
                possible_moves.append((piece.row, piece.col))
        return possible_moves

    def next_state(self, piece_matrix, position):
        """
        Placed a black piece at the given position
        :param piece_matrix: the state that you want to be updated
        :param position: the position that you want to place the black piece at
        :return: the new state with the black piece placed at the given position
        """
        piece_matrix[position[0]][position[1]].colour = Colour.BLACK
        return piece_matrix

    def remove_captured_groups_from_board(self, piece_matrix):
        """
        Removes all captured pieces in this state.
        First removes all of the opponent pieces that have no liberties left and then removes all pieces of the current
        colour that have no liberties left.
        :param piece_matrix: The state that you want to remove all of the captured pieces from
        :return: the new state that has any pieces that were captured removed
        """
        groups = self.get_all_groups_on_board(piece_matrix)
        groups = [group for group in groups if group != []]
        for group in groups:
            if len(group) > 0:
                if group[0].colour == self.opposite_colour:
                    if group[0].colour != Colour.Ko:
                        liberties = self.get_liberties_for_group(group)
                        if len(liberties) == 0:
                            self.killed_groups.append(copy.deepcopy(group))
                            remove_pieces(group)

        for group in groups:
            if len(group) > 0:
                if (
                    group[0].colour != self.opposite_colour
                    and group[0].colour != Colour.CLEAR
                ):
                    if group[0].colour != Colour.Ko:
                        liberties = self.get_liberties_for_group(group)
                        if len(liberties) == 0:
                            self.killed_groups.append(copy.deepcopy(group))
                            remove_pieces(group)
        return piece_matrix

    def get_number_of_black_pieces(self, piece_matrix) -> int:
        """
        goes through the board and sums up the number of black pieces on the board
        :param piece_matrix: state that you want to check for black pieces
        :return: the number of black pieces on the board in this state
        """
        sum = 0
        for row in piece_matrix:
            for piece in row:
                if piece.colour == Colour.BLACK:
                    sum += 1
        return sum

    def get_number_of_white_pieces(self, piece_matrix) -> int:
        """
        goes through the board and sums up the number of white pieces on the board
        :param piece_matrix: state that you want to check for white pieces
        :return: the number of white pieces on the board in this state
        """
        total = 0
        for row in piece_matrix:
            for piece in row:
                if piece.colour == Colour.WHITE:
                    total += 1
        return total

    def get_black_territory(self, piece_matrix) -> int:
        """
        Defining black territory as any empty spot that is fully surrounded by only black
        """
        total = 0
        for row in range(len(piece_matrix)):
            for col in range(len(piece_matrix[row])):
                if piece_matrix[row][col].colour == Colour.CLEAR and len(
                    self.get_adjacent_of_colour(row, col, Colour.BLACK)
                ):
                    total += 1
        return total

    def get_white_territory(self, piece_matrix) -> int:
        """
        Defining white territory as any empty spot that is fully surrounded by only white
        """
        total = 0
        for row in range(len(piece_matrix)):
            for col in range(len(piece_matrix[row])):
                if piece_matrix[row][col].colour == Colour.CLEAR and len(
                    self.get_adjacent_of_colour(row, col, Colour.WHITE)
                ):
                    total += 1
        return total

    def score(self, piece_matrix) -> int:
        """
        returns an integer representation of how the game is approximately going
        black will have a positive when they are winning and will return a negative value if white is winning
        if 0 is returned then the game is fairly simple
        the function is kept fairly simple as it will be called a lot inside of the minimax algorithm so needs to be
        as fast as possible
        """
        return (
            self.get_number_of_black_pieces(piece_matrix)
            + self.get_black_territory(piece_matrix)
            - self.get_number_of_white_pieces(piece_matrix)
            - self.get_white_territory(piece_matrix)
        )

    def get_territory_for_black(self, piece_matrix) -> int:
        """
        Gets territory for black by only counting empty spaces where at least two of the pieces beside it are also black
        :param piece_matrix: the state that you want to check blacks territory for
        :return: returns the amount of territory that black has as an integer
        """
        total = 0
        for row in piece_matrix:
            for piece in row:
                if piece.colour == Colour.CLEAR:
                    liberties = self.get_adjacent_of_colour(
                        piece.row, piece.col, Colour.BLACK
                    )
                    if len(liberties) > 2:
                        total += 1
        return total

    def get_territory_for_white(self, piece_matrix) -> int:
        """
        Gets territory for white by only counting empty spaces where at least two of the pieces beside it are also white
        :param piece_matrix: the state that you want to check whites territory for
        :return: returns the amount of territory that white has as an integer
        """
        total = 0
        for row in piece_matrix:
            for piece in row:
                if piece.colour == Colour.CLEAR:
                    liberties = self.get_adjacent_of_colour(
                        piece.row, piece.col, Colour.WHITE
                    )
                    if len(liberties) > 2:
                        total += 1
        return total
