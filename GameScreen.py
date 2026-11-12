import pygame
import os
import sys
from Settings import WIDTH, HEIGHT, WHITE


class GameScreen:
    # --- Klasa bazowa dla wszystkich ekranów ---
    def __init__(self, bg_image_name):
        try:
            self.bg = pygame.image.load(os.path.join("Images", bg_image_name)).convert()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((20, 20, 20))

        try:
            self.score_font = pygame.font.Font("Font/Tiny5-Regular.ttf", 45)
        except:
            self.score_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.font_big = pygame.font.SysFont("Impact", 80)
        self.font_mid = pygame.font.SysFont("Impact", 50)
        self.font_small = pygame.font.SysFont("Impact", 20)

        BUTTON_SIZE = (180, 70)

        self.start_idle = pygame.transform.scale(
            pygame.image.load("Images/Start_0.png").convert_alpha(), BUTTON_SIZE)
        self.start_hover = pygame.transform.scale(
            pygame.image.load("Images/Start_1.png").convert_alpha(), BUTTON_SIZE)

        self.quit_idle = pygame.transform.scale(
            pygame.image.load("Images/Quit_0.png").convert_alpha(), BUTTON_SIZE)
        self.quit_hover = pygame.transform.scale(
            pygame.image.load("Images/Quit_1.png").convert_alpha(), BUTTON_SIZE)

        self.highscore_idle = pygame.transform.scale(
            pygame.image.load("Images/Highscore_0.png").convert_alpha(), BUTTON_SIZE)
        self.highscore_hover = pygame.transform.scale(
            pygame.image.load("Images/Highscore_1.png").convert_alpha(), BUTTON_SIZE)

        # 3. Definicja prostokątów
        self.start_rect = self.start_idle.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.quit_rect = self.quit_idle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 165))
        self.highscore_rect = self.highscore_idle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))


class StartScreen(GameScreen):
    def __init__(self):
        super().__init__("tło.png")
        self.hover_sound = pygame.mixer.Sound("Audio/click.wav")
        self.hover_sound.set_volume(0.5)
        self.start_hovered = False
        self.quit_hovered = False
        self.highscore_hovered = False

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        title_surf = self.font_big.render("SEAQUEST", True, (255, 255, 0))
        self.title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 10))
        screen.blit(title_surf, self.title_rect)

        # LOGIKA PRZYCISKU START
        if self.start_rect.collidepoint(mouse_pos):
            screen.blit(self.start_hover, self.start_rect)
            if not self.start_hovered:
                self.hover_sound.play()
                self.start_hovered = True
        else:
            screen.blit(self.start_idle, self.start_rect)
            self.start_hovered = False

            # LOGIKA PRZYCISKU QUIT
        if self.quit_rect.collidepoint(mouse_pos):
            screen.blit(self.quit_hover, self.quit_rect)
            if not self.quit_hovered:
                self.hover_sound.play()
                self.quit_hovered = True
        else:
            screen.blit(self.quit_idle, self.quit_rect)
            self.quit_hovered = False

            # LOGIKA PRZYCISKU HIGHSCORE
        if self.highscore_rect.collidepoint(mouse_pos):
            screen.blit(self.highscore_hover, self.highscore_rect)
            if not self.highscore_hovered:
                self.hover_sound.play()
                self.highscore_hovered = True
        else:
            screen.blit(self.highscore_idle, self.highscore_rect)
            self.highscore_hovered = False


class HighscoreScreen(GameScreen):
    def __init__(self, top_score):
        super().__init__("highscore_bg.png")
        self.top_score = top_score

    def draw(self, screen):
        # 1. Rysujemy tło
        screen.blit(self.bg, (0, 0))

        score_str = str(self.top_score).zfill(7)
        score_surf = self.score_font.render(score_str, True, (255, 215, 0))

        score_rect = score_surf.get_rect(center=(WIDTH // 2 - 4, HEIGHT // 2 + 32))
        screen.blit(score_surf, score_rect)

        if (pygame.time.get_ticks() // 500) % 2 == 0:
            hint_surf = self.font_small.render("PRESS ANY KEY TO RETURN", True, WHITE)
            hint_rect = hint_surf.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            screen.blit(hint_surf, hint_rect)


class WinScreen(GameScreen):
    def __init__(self, score):
        super().__init__("tło_win.png")
        self.score = score

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        score_surf = self.font_mid.render(f"SCORE: {self.score}", True, WHITE)
        score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        screen.blit(score_surf, score_rect)


class LoseScreen(GameScreen):
    def __init__(self, score):
        super().__init__("tło_lose.png")
        self.score = score

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        score_surf = self.font_mid.render(f"FINAL SCORE: {self.score}", True, (255, 50, 50))
        score_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        screen.blit(score_surf, score_rect)