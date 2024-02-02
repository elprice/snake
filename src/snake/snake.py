import sys
from typing import Dict

import pygame


def run() -> None:
    pygame.init()
    vec = pygame.math.Vector2  # 2 for two dimensional

    HEIGHT = 400
    WIDTH = 400
    fps = 10
    clock = pygame.time.Clock()
    clock.tick(fps)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    BLACK = (0, 0, 0)
    GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    # key: action
    controls: Dict[int, tuple] = {
        pygame.K_RIGHT: GRAY,
        pygame.K_LEFT: YELLOW,
        pygame.K_UP: CYAN,
        pygame.K_DOWN: MAGENTA,
    }

    snake = []
    segment_size = 20
    snake_direction = "right"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                for key, val in controls.items():
                    if event.key == key:
                        # screen.fill(val)
                        # Create a surface and pass in a tuple containing its length and width
                        surf = pygame.Surface((50, 50))

                        # Give the surface a color to separate it from the background
                        surf.fill((255, 255, 255))
                        screen.blit(surf, (HEIGHT / 2, WIDTH / 2))
                        pygame.display.flip()
                        pygame.display.update()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
