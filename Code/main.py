from os import system
import pygame
from pygame.constants import FULLSCREEN, RESIZABLE
from board import Board
import pygame_gui

def main():
    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("test program")

    screen = pygame.display.set_mode((800,800), RESIZABLE)

    running = True
    background = pygame.image.load("Assets//background.jpg")
    board = Board(background=background, size=19)
    manager = pygame_gui.UIManager((800, 800))
    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                             text='Say Hello',
                                             manager=manager)
    clock = pygame.time.Clock()
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                if width < 800:
                    width = 800
                if height < 800:
                    height = 800
                screen = pygame.display.set_mode((width,height), RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.checkMousePosition(pygame.mouse.get_pos())
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == hello_button:
                        print("hello world")
            manager.process_events(event)
        manager.update(time_delta)
            
        screen.fill((255,255,255))
        board.render(screen)
        manager.draw_ui(screen)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == '__main__':
    main()