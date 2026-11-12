import pygame
import os
import random
from Settings import WIDTH, HEIGHT, WATER_LINE


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_prefix, speed_min, speed_max, scale=(50, 40)):
        super().__init__()
        self.frames_right = []
        self.frames_left = []

        for i in range(3):
            try:
                path = os.path.join("Images", f"{image_prefix}{i}.png")
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, scale)
                self.frames_right.append(img)
                self.frames_left.append(pygame.transform.flip(img, True, False))
            except Exception as e:
                surf = pygame.Surface(scale)
                surf.fill((255, 0, 0))
                self.frames_right.append(surf)
                self.frames_left.append(surf)

        self.current_frame = 0
        self.animation_speed = 0.10

        # Losowanie strony pojawienia się
        self.facing = random.choice(["left", "right"])
        if self.facing == "left":
            self.rect = self.frames_left[0].get_rect(x=WIDTH + 50)
            self.speed_x = -random.randint(speed_min, speed_max)
        else:
            self.rect = self.frames_right[0].get_rect(x=-50)
            self.speed_x = random.randint(speed_min, speed_max)

        self.rect.y = random.randint(WATER_LINE + 50, HEIGHT - 50)
        self.image = self.frames_right[0] if self.facing == "right" else self.frames_left[0]

    def base_update(self):
        # --- Obsługuje wspólny ruch i animację dla wszystkich ryb ---
        self.rect.x += self.speed_x

        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames_right):
            self.current_frame = 0

        idx = int(self.current_frame)
        self.image = self.frames_right[idx] if self.facing == "right" else self.frames_left[idx]

        if self.rect.right < -150 or self.rect.left > WIDTH + 150:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        try:
            path = os.path.join("Images", "small_shoot.png")
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (15, 15))
            if direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        except:
            self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 5)

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 12 * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()


class SmallAggressive(Enemy):
    def __init__(self):
        super().__init__("small_enemy", 3, 3)
        self.hp = 1
        # Mechanizm strzelania
        self.shoot_delay = 1000
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.base_update()
        # Logika strzelania
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return True
        return False


class MediumAggressive(Enemy):
    """Średni przeciwnik - płynie umiarkowanie szybko i strzela serią"""

    def __init__(self):
        super().__init__("mid_agres", 2, 4, scale=(70, 50))

        self.shoot_delay = 1500
        self.last_shot = pygame.time.get_ticks()
        self.hp = 2
        # Logika serii strzałów
        self.is_bursting = False
        self.burst_count = 0
        self.last_burst_time = 0

    def update(self):
        self.base_update()
        now = pygame.time.get_ticks()
        # Sprawdzanie głównego czasu przeładowania
        if not self.is_bursting and now - self.last_shot > self.shoot_delay:
            self.is_bursting = True
            self.burst_count = 0
            self.last_shot = now

        # Logika serii strzału
        if self.is_bursting:
            if now - self.last_burst_time > 300:
                self.last_burst_time = now
                self.burst_count += 1

                if self.burst_count >= 2:
                    self.is_bursting = False

                return True

        return False


class BigAggressive(Enemy):
    def __init__(self):
        super().__init__("Big_agres", 1, 2, scale=(100, 60))

        self.hp = 3
        self.score_value = 60
        self.oxygen_damage = 33

    def update(self):
        self.base_update()
        return False