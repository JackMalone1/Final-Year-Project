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


def get_adjacent_pieces_of_same_colour(board: Board, row: int, col: int) -> list[Piece]:
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

