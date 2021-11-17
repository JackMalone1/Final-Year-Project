from typing import Tuple
from piece import piece
import pygame
from colours import Colour

class Board:
    def __init__(self, background: pygame.image, size: int):
        self.background = background
        self.background_rect = background.get_rect()
        self.size = size
        w, h = pygame.display.get_surface().get_size()
        self.tile_size = (w / self.size) * 0.9        
        self.offset = 30
        self.set_up_grid()
        self.piece_matrix = [[piece((-10,-10), Colour.CLEAR) for x in range(self.size + 1)] for y in range(self.size + 1)]
        print(self.piece_matrix)

    def render(self, screen: pygame.display) -> None:
        screen.blit(self.background, self.background_rect)
        [[pygame.draw.rect(screen, pygame.Color(0,0,0), col, 3) for col in row] for row in self.board]
        
        for row in self.piece_matrix:
            for piece in row:
                piece.render(screen)

    def checkMousePosition(self, mouse_position):
        for x in range(self.size + 1):
            for y in range(self.size + 1):
                if self.board_intersections[x][y].collidepoint(mouse_position):
                    print("Collision")
                    self.piece_matrix[x][y].position = self.board_intersections[x][y].center


    def set_up_grid(self):
        self.board = [[0 for x in range(self.size)] for y in range(self.size)]
        self.board_intersections = [[0 for x in range(self.size + 1)] for y in range(self.size + 1)]       
        for y in range(self.size + 1):
            y_position = self.offset + (y * self.tile_size)
            for x in range(self.size + 1):
                if(x < self.size and y < self.size):
                    x_position = self.offset + (x * self.tile_size)
                    rect = pygame.Rect(x_position, y_position, self.tile_size, self.tile_size)
                    intersection = pygame.Rect(x_position - 5, y_position - 5, 10, 10)
                    self.board[x][y] = rect
                    self.board_intersections[x][y] = intersection
                else:
                    x_position = self.offset + (x * self.tile_size)
                    intersection = pygame.Rect(x_position - 5, y_position - 5, 10, 10)
                    self.board_intersections[x][y] = intersection

