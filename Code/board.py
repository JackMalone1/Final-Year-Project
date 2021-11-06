from typing import Tuple
import pygame

class Board:
    def __init__(self, background: pygame.image, size: int):
        self.background = background
        self.background_rect = background.get_rect()
        self.size = size
        w, h = pygame.display.get_surface().get_size()
        self.tile_size = (w / self.size) * 0.9
        self.set_up_grid()

    def render(self, screen: pygame.display) -> None:
        screen.blit(self.background, self.background_rect)
        for row in self.board:
            for col in row:
                pygame.draw.rect(screen, pygame.Color(0,0,0), col, 3)
            

    def set_up_grid(self):
        self.board = [[0 for x in range(self.size)] for y in range(self.size)]

        for y in range(self.size):
            y_position = 10 + (y * self.tile_size)

            for x in range(self.size):
                x_position = 10 + (x * self.tile_size)
                rect = pygame.Rect(x_position, y_position, self.tile_size, self.tile_size)
                self.board[x][y] = rect
                 
