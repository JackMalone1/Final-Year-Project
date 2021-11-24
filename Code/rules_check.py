from board import Board
from colours import Colour
from piece import Piece


def is_koish(board: Board, row: int, col: int) -> Colour:
    piece = board.get_piece_at_position(row, col)
    if piece.colour is not Colour.CLEAR:
        return None
    colour = Colour.CLEAR
    if row - 1 > 0 and board.get_piece_at_position(row - 1, col).colour is not Colour.CLEAR:
        colour = board.get_piece_at_position(row - 1, col).colour
    if col - 1 > 0 and board.get_piece_at_position(row, col - 1).colour is not colour:
        return None
    if row + 1 < board.size and board.get_piece_at_position(row + 1, col).colour is not colour:
        return None
    if col + 1 < board.size and board.get_piece_at_position(row, col + 1).colour is not colour:
        return None
    return colour


def get_adjacent_pieces_of_same_colour(board: Board, row: int, col: int) -> list:
    adjacent_pieces = []
    colour = board.get_piece_at_position(row, col).colour
    if row - 1 > 0 and board.get_piece_at_position(row - 1, col).colour is colour:
        adjacent_pieces.append(board.get_piece_at_position(row - 1, col))
    if col - 1 > 0 and board.get_piece_at_position(row, col - 1).colour is colour:
        adjacent_pieces.append(board.get_piece_at_position(row, col - 1))
    if row + 1 < board.size and board.get_piece_at_position(row + 1, col).colour is colour:
        adjacent_pieces.append(board.get_piece_at_position(row + 1, col))
    if col + 1 < board.size and board.get_piece_at_position(row, col + 1).colour is colour:
        adjacent_pieces.append(board.get_piece_at_position(row, col + 1))
    return adjacent_pieces


def get_adjacent_of_colour(board: Board, row: int, col: int, colour: Colour) -> list:
    adjacent_pieces = []
    if row - 1 > 0 and board.get_piece_at_position(row - 1, col).colour is colour:
        adjacent_pieces.append(board.get_piece_at_position(row - 1, col))
    if col - 1 > 0 and board.get_piece_at_position(row, col - 1).colour is colour:
        adjacent_pieces.append(board.get_piece_at_position(row, col - 1))
    if row + 1 < board.size and board.get_piece_at_position(row + 1, col).colour is colour:
        adjacent_pieces.append(board.get_piece_at_position(row + 1, col))
    if col + 1 < board.size and board.get_piece_at_position(row, col + 1).colour is colour:
        adjacent_pieces.append(board.get_piece_at_position(row, col + 1))
    return adjacent_pieces


def is_move_legal(board: Board, position: tuple, colour: Colour) -> bool:
    if board.get_piece_at_position(position[0], position[1]).colour is not Colour.CLEAR:
        return False
    return True


def get_liberties_for_group(board: Board, group: list[Piece]) -> set:
    liberties = set()

    for piece in group:
        piece_liberties = get_adjacent_of_colour(board, piece.row, piece.col)
        [liberties.add(liberty) for liberty in piece_liberties]

    return liberties
