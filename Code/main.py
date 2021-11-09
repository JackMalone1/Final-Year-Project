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
        pygame.event.pump()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
                running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            if width < 800:
                width = 800
            if height < 800:
                height = 800
            screen = pygame.display.set_mode((width,height), RESIZABLE)
            
        screen.fill((255,255,255))
        board.render(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()