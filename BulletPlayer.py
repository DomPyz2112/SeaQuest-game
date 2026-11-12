import pygame
import os
from Settings import WIDTH, HEIGHT, WATER_LINE

class Bullet_player(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.frames = []

        # Ładowanie klatek animacji strzału
        for i in range(0, 3):
            path = os.path.join("Images", f"player_shoot{i}.png")
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (40, 30))

            if direction == "right":
                img = pygame.transform.flip(img, True, False)
            self.frames.append(img)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]

        if direction == "left":
            self.rect = self.image.get_rect(midleft=(x, y))
        else:
            self.rect = self.image.get_rect(midright=(x, y))

        self.direction = direction
        self.speed = 12

    def update(self):
        # Ruch pocisku
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        # Animacja pocisku
        self.current_frame += 0.2
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

        # Usuń pocisk, jeśli wyleci poza ekran
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.kill()