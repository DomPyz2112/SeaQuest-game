import pygame
import random
import os
from Settings import WIDTH, HEIGHT, WATER_LINE

class Diver(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = []

        for i in range(3):
            img = pygame.image.load(f"Images/plywak{i}.png").convert_alpha()
            self.frames.append(pygame.transform.scale(img, (100, 50)))

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 0.075
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        self.current_frame += self.animation_speed

        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        if self.rect.right < 0:
            self.kill()