import pygame
import random
import os
from Settings import WIDTH, HEIGHT, WATER_LINE


class GoldenFish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames_right = []
        self.frames_left = []

        file_names = ["złota0.png", "złota1.png", "złota2.png"]

        for name in file_names:
            try:
                img = pygame.image.load(os.path.join("Images", name)).convert_alpha()
                img = pygame.transform.scale(img, (40, 30))
                self.frames_left.append(img)
                self.frames_right.append(pygame.transform.flip(img, True, False))
            except:
                surf = pygame.Surface((40, 30))
                surf.fill((255, 255, 0))
                self.frames_right.append(surf)
                self.frames_left.append(surf)


        self.current_frame = 0
        self.animation_speed = 0.15

        self.rect = self.frames_right[0].get_rect()
        self.rect.y = random.randint(WATER_LINE + 50, HEIGHT - 50)

        if random.choice(["left", "right"]) == "left":
            self.rect.x = -50
            self.speed_x = random.randint(2, 4)
            self.facing = "left"
        else:
            self.rect.x = WIDTH + 50
            self.speed_x = random.randint(-4, -2)
            self.facing = "right"

        self.image = self.frames_right[0]

    def update(self):
        self.rect.x += self.speed_x

        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames_right):
            self.current_frame = 0

        idx = int(self.current_frame)
        if self.facing == "right":
            self.image = self.frames_right[idx]
        else:
            self.image = self.frames_left[idx]

        if self.rect.right < -100 or self.rect.left > WIDTH + 100:
            self.kill()
