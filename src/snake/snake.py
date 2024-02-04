import logging
import random
import sys
import time
from typing import Dict, List, Optional, Tuple

import pygame
from pygame.key import ScancodeWrapper
from pygame.rect import Rect

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def run() -> None:
    pygame.init()

    HEIGHT = 400
    WIDTH = 400

    fps = 60
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game")

    BLACK = (0, 0, 0)
    GRAY = (127, 127, 127)
    WHITE = (255, 255, 255)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    BACKGROUND = BLACK

    # key: direction
    controls: Dict[int, tuple] = {
        pygame.K_RIGHT: (1, 0),
        pygame.K_LEFT: (-1, 0),
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),  # weird direction because of window x,y
    }

    blocked: Dict[Tuple[int, int], Tuple[int, int]] = {
        (1, 0): (-1, 0),
        (-1, 0): (1, 0),
        (0, 1): (0, -1),
        (0, -1): (0, 1),
    }

    class Segment(pygame.sprite.Sprite):
        def __init__(self, pos_x: int, pos_y: int, segment_size: int = 20) -> None:
            super(Segment, self).__init__()
            self.segment_size = segment_size
            self.next: Optional[Segment | None] = None
            self.surf = pygame.Surface((segment_size, segment_size))
            self.surf.fill(MAGENTA)
            self.rect = self.surf.get_rect(
                x=pos_x,
                y=pos_y,
            )

    class Snake(pygame.sprite.Sprite):
        def __init__(self, size: int = 20) -> None:
            super(Snake, self).__init__()
            self.size = size
            self.next: Optional[Segment | None] = None
            self.direction = controls[pygame.K_RIGHT]
            self.next_direction = self.direction
            self.surf = pygame.Surface((size, size))
            self.surf.fill(WHITE)
            self.rect = self.surf.get_rect(x=self.size, y=self.size)

        def grow(self) -> None:
            curr = self.next
            x = self.rect.x - (self.direction[0] * self.size)
            y = self.rect.y - (self.direction[1] * self.size)
            self.next = Segment(pos_x=x, pos_y=y)
            self.next.next = curr

        def update_next_direction(self, pressed_keys: ScancodeWrapper) -> None:
            for key, direction in controls.items():
                if pressed_keys[key]:
                    self.next_direction = direction

        def update_position(self) -> None:
            if self.next_direction != blocked[self.direction]:
                self.direction = self.next_direction
            curr = self.next
            prev = self.rect
            while curr:
                temp = curr.rect
                curr.rect = curr.surf.get_rect(x=prev.x, y=prev.y)
                prev = temp
                curr = curr.next

            self.rect.move_ip(*[self.size * mod for mod in self.direction])

    class Apple(pygame.sprite.Sprite):
        def __init__(self, size: int = 20) -> None:
            super(Apple, self).__init__()
            self.size = size
            self.direction = controls[pygame.K_RIGHT]
            self.surf = pygame.Surface((size, size))
            self.surf.fill(CYAN)
            self.rect = self.get_new_position()

        def get_new_position(self) -> Rect:
            return self.surf.get_rect(
                x=random.randrange(self.size, WIDTH - self.size, self.size),
                y=random.randrange(self.size, HEIGHT - self.size, self.size),
            )

    class Wall(pygame.sprite.Sprite):
        def __init__(self, pos_x: int, pos_y: int, size: int = 20) -> None:
            super(Wall, self).__init__()
            self.size = size
            self.surf = pygame.Surface((size, size))
            self.surf.fill(GRAY)
            self.rect = self.surf.get_rect(x=pos_x, y=pos_y)

    snake = Snake()
    apple = Apple()

    wallsize = 20
    walls = []

    for x in range(0, WIDTH, wallsize):
        for y in range(0, HEIGHT, wallsize):
            if x == 0 or y == 0 or x == WIDTH - wallsize or y == HEIGHT - wallsize:
                walls.append(Wall(pos_x=x, pos_y=y))

    grows = pygame.sprite.Group([apple])
    kills = pygame.sprite.Group(walls)

    frames = 0
    snake_update_frames = fps // 6

    # draw everything
    sprites: List[pygame.sprite.Sprite.Sprite] = [snake, apple, *walls]
    for sprite in sprites:
        screen.blit(sprite.surf, sprite.rect)

    curr = time.time()
    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()

        if not (frames + 1) % snake_update_frames:
            now = time.time()
            # print(now - curr)
            curr = now
            snake.update_position()

            if pygame.sprite.spritecollide(snake, grows, False):
                log.info("Ate an apple.")
                snake.grow()
                kills.add(snake.next)
                snake.grow()
                kills.add(snake.next)
                snake.grow()
                kills.add(snake.next)
                snake.grow()
                kills.add(snake.next)
                snake.grow()
                kills.add(snake.next)

                while pygame.sprite.spritecollide(
                    apple, [*kills, snake], False
                ):  # this could just be all non-apple sprites
                    log.info("Generated a new apple.")
                    apple.kill()
                    apple = Apple()
                    log.info(apple.rect)
                    grows.add(apple)
            if pygame.sprite.spritecollide(snake, kills, False):
                sys.exit()

            screen.fill(BACKGROUND)
            screen.blit(snake.surf, snake.rect)
            segment = snake.next
            while segment:
                # print(f"drawing {segment.rect}")
                screen.blit(segment.surf, segment.rect)
                segment = segment.next
            screen.blit(apple.surf, apple.rect)
            for wall in walls:
                screen.blit(wall.surf, wall.rect)

        pressed_keys = pygame.key.get_pressed()
        snake.update_next_direction(pressed_keys)

        pygame.display.flip()
        # print(frames)
        frames += 1
