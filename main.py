"""
main.py — PROVIDED (do not modify)

Entry point: initialises pygame, creates the window, and runs the game loop
at 60 fps.  All game logic lives in Game/Board; all drawing lives in Renderer.
"""

import pygame
from game import Game
from renderer import Renderer

WINDOW_SIZE = 640   # 8 squares × 80 px
FPS = 60


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 40))  # +40 for status bar
    pygame.display.set_caption("Chess")

    game = Game()
    renderer = Renderer(screen)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.handle_click(event.pos)

        renderer.draw(game)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
