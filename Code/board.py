import pygame

class Board:
    def __init__(self, background: pygame.image, size: int):
        self.background = background
        self.background_rect = background.get_rect()
        self.size = size

    def render(self, screen: pygame.display) -> None:
        screen.blit(self.background, self.background_rect)
