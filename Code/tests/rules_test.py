import unittest

from player_turn import player_turn
from rules_check import *
from board import Board
import pygame
from pygame.constants import FULLSCREEN, RESIZABLE


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertIsNot(True, False)

    def test_legal_moves(self):
        pygame.init()

        pygame.display.set_caption("test program")

        screen = pygame.display.set_mode((800, 800), RESIZABLE)
        background = pygame.image.load("..//Assets//background.jpg")
        board = Board(background=background, size=19, font_path="../MONOFONT.ttf",
                      piece_sound_effect_path="../Assets/Sounds/place_piece.ogg")
        self.assertEqual(is_move_legal(board, (1, 1), Colour.BLACK), True)
        board.place_piece_at_position(player_turn.BLACK, (1, 1))
        self.assertEqual(is_move_legal(board, (1, 1), Colour.BLACK), False)  # can't place on occupied position


if __name__ == '__main__':
    unittest.main()
