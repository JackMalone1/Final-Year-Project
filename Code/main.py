import pygame
from pygame.constants import FULLSCREEN, RESIZABLE

def main():
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("test program")

    screen = pygame.display.set_mode((800,600), RESIZABLE)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255,255,255))
        pygame.draw.rect(screen, (0,0,255),(200,150,100,50))
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()