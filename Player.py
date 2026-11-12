import pygame
import random
import os
from BulletPlayer import Bullet_player
from Settings import WIDTH, HEIGHT, WATER_LINE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.score = 0
        self.frames_right = []
        self.frames_left = []
        self.saved_divers = 0
        file_names = ["submarine.png", "submarine1.png"]
        self.shoot_sound = pygame.mixer.Sound(os.path.join("Audio", "submarine_shot.wav"))
        self.shoot_sound.set_volume(0.3)


        for name in file_names:
            img_path = os.path.join("Images", name)
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (60, 60))

            self.frames_right.append(img)
            self.frames_left.append(pygame.transform.flip(img, True, False))

        self.current_frame = 0
        self.animation_speed = 0.1
        self.direction = "right"

        self.image = self.frames_right[self.current_frame]
        self.rect = self.image.get_rect(center=(WIDTH // 4, HEIGHT // 2))

        self.oxygen = 100
        self.max_oxygen = 100
        self.speed = 5
        self.WATER_LINE = WATER_LINE

        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.shoot_delay = 100

    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames_right):
            self.current_frame = 0


        if self.direction == "left":
            self.image = self.frames_right[int(self.current_frame)]
        else:
            self.image = self.frames_left[int(self.current_frame)]

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now

            # Ustalamy punkt startowy pocisku
            bullet_y = self.rect.centery + 18

            if self.direction == "right":
                bullet_x = self.rect.right - 5
                new_bullet = Bullet_player(bullet_x, bullet_y, "right")
            else:
                bullet_x = self.rect.left + 5
                new_bullet = Bullet_player(bullet_x, bullet_y, "left")

            self.bullets.add(new_bullet)
            self.shoot_sound.play()

    def update(self):
        keys = pygame.key.get_pressed()


        if keys[pygame.K_UP] and self.rect.top > self.WATER_LINE:
            self.rect.y -= self.speed

        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = "left"

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.direction = "right"

        is_underwater = self.rect.top > self.WATER_LINE
        if is_underwater:
            self.oxygen -= 0.1
        else:
            self.oxygen += 0.5

        self.oxygen = max(0, min(self.oxygen, self.max_oxygen))
        self.animate()