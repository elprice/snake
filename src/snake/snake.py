import random
import sys
import time
from typing import Dict, Optional

import pygame
from pygame.key import ScancodeWrapper
from pygame.rect import Rect


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
    YELLOW = (255, 255, 0)
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

    class Segment(pygame.sprite.Sprite):
        def __init__(self, rect: Rect, segment_size: int = 20) -> None:
            super(Segment, self).__init__()
            self.segment_size = segment_size
            self.next: Optional[Segment | None] = None
            self.surf = pygame.Surface((segment_size, segment_size))
            self.surf.fill(MAGENTA)
            self.rect = self.surf.get_rect(
                x=rect.x,
                y=rect.y,
            )

    class Snake(pygame.sprite.Sprite):
        def __init__(self, size: int = 20) -> None:
            super(Snake, self).__init__()
            self.size = size
            self.next: Optional[Segment | None] = None
            self.direction = controls[pygame.K_RIGHT]
            self.surf = pygame.Surface((size, size))
            self.surf.fill(WHITE)
            self.rect = self.surf.get_rect()

        def grow(self) -> None:
            current = self.next
            print(self.rect)
            rect = self.surf.get_rect(
                x=self.rect.x - (self.direction[0] * self.size),
                y=self.rect.y - (self.direction[1] * self.size),
            )
            print(self.rect)

            self.next = Segment(rect)
            self.next.next = current

        def update_direction(self, pressed_keys: ScancodeWrapper) -> None:
            for key, direction in controls.items():
                if pressed_keys[key]:
                    self.direction = direction

        def update_position(self) -> None:
            segment = self.next
            prev_rect = self.rect
            while segment:
                temp = segment.rect
                segment.rect = segment.surf.get_rect(x=prev_rect.x, y=prev_rect.y)
                prev_rect = temp
                print(segment.rect)
                segment = segment.next

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
                x=random.randrange(0, WIDTH // self.size) * self.size,
                y=random.randrange(0, HEIGHT // self.size) * self.size,
            )

        # def update(self) -> None:
        #    screen.blit(self.surf, self.rect)

    snake = Snake()
    apple = Apple()
    not_snake = pygame.sprite.Group()
    not_snake.add(apple)

    frames = 0
    snake_update_frames = fps // 4  # once per second
    print(snake_update_frames)
    screen.blit(snake.surf, snake.rect)
    screen.blit(apple.surf, apple.rect)
    curr = time.time()
    while True:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not (frames + 1) % snake_update_frames:
            now = time.time()
            print(now - curr)
            curr = now
            snake.update_position()
            if pygame.sprite.spritecollide(snake, not_snake, False):
                print("YES")
                snake.grow()
                while pygame.sprite.spritecollide(snake, not_snake, True):
                    print("NO")
                    apple = Apple()
                    not_snake.add(apple)

            screen.fill(BACKGROUND)
            screen.blit(snake.surf, snake.rect)
            segment = snake.next
            while segment:
                # print(f"drawing {segment.rect}")
                screen.blit(segment.surf, segment.rect)
                segment = segment.next
            screen.blit(apple.surf, apple.rect)

        pressed_keys = pygame.key.get_pressed()
        snake.update_direction(pressed_keys)

        pygame.display.flip()
        # print(frames)
        frames += 1
