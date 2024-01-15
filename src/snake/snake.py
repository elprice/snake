import sys
from typing import Dict

import pygame


def run():
    pygame.init()
    vec = pygame.math.Vector2  # 2 for two dimensional

    HEIGHT = 450
    WIDTH = 400
    ACC = 0.5
    FRIC = -0.12
    FPS = 60

    FramePerSec = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    BLACK = (0, 0, 0)
    GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    controls: Dict[int, tuple] = {
        pygame.K_RIGHT: GRAY,
        pygame.K_LEFT: YELLOW,
        pygame.K_UP: CYAN,
        pygame.K_DOWN: MAGENTA,
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                for key, val in controls.items():
                    if event.key == key:
                        screen.fill(val)
                        pygame.display.update()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
