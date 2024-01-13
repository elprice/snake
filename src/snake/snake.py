import sys

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

    displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
