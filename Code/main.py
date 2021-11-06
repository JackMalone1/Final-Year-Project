from os import system
import pygame
from pygame.constants import FULLSCREEN, RESIZABLE
from board import Board

def main():
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("test program")

    screen = pygame.display.set_mode((800,800), RESIZABLE)

    running = True
    background = pygame.image.load("Assets//background.jpg")
    board = Board(background=background, size=19)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255,255,255))
        board.render(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()