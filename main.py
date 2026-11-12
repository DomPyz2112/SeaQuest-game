import pygame
import os
import sys
import random

from Settings import WIDTH, WATER_LINE, HEIGHT, FPS, WHITE, RED, GREEN, BLACK
from Player import Player
from Diver import Diver
from Booster import GoldenFish
from Enemies import SmallAggressive, MediumAggressive, BigAggressive, EnemyBullet
from GameScreen import StartScreen, WinScreen, LoseScreen, HighscoreScreen
from ScoreManager import ScoreManager

# --- KLASA KONFIGURACJI POZIOMU ---

class LevelConfig:
    def __init__(self, number, spawn_delay, bg_file):
        self.number = number
        self.spawn_delay = spawn_delay
        self.bg_file = bg_file

# --- FUNKCJE POMOCNICZE UI ---

def draw_bar(screen, x, y, current_val, max_val, img_full, img_empty):
    screen.blit(img_empty, (x, y))
    ratio = max(0, current_val / max_val)
    width_to_show = int(img_full.get_width() * ratio)
    clip_rect = pygame.Rect(0, 0, width_to_show, img_full.get_height())
    screen.blit(img_full, (x, y), clip_rect)

def draw_ui(screen, player, bar_full, bar_empty, diver_icon, level_num):
    font = pygame.font.SysFont("Impact", 24)
    try:
        score_font = pygame.font.Font("Font/Tiny5-Regular.ttf", 50)
    except:
        score_font = pygame.font.SysFont("Arial", 40, bold=True)

    # 1. Formatowanie wyniku
    score_str = str(player.score).zfill(7)
    score_text = score_font.render(score_str, True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, 35))
    screen.blit(score_text, score_rect)

    # 2. Pasek tlenu
    draw_bar(screen, 20, 5, player.oxygen, player.max_oxygen, bar_full, bar_empty)

    # 3. Ikony nurków
    start_x = WIDTH - 60
    spacing = 55
    for i in range(player.saved_divers):
        icon_x = start_x - (i * spacing)
        screen.blit(diver_icon, (icon_x, 20))

# --- GŁÓWNA FUNKCJA GRY ---

def main():
    pygame.init()
    pygame.mixer.init()
    score_manager = ScoreManager()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Seaquest Clone - High Performance Version")
    clock = pygame.time.Clock()

    # 1. MUZYKA I DŹWIĘKI
    music_path = os.path.join("Audio", "background_sound.mp3")
    if os.path.exists(music_path):
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

    try:
        shoot_sound = pygame.mixer.Sound(os.path.join("Audio", "shoot.wav"))
        shoot_sound.set_volume(0.1)
    except:
        shoot_sound = None

    # 2. PRE-LOADING ZASOBÓW
    tlen_full = pygame.transform.scale(pygame.image.load("Images/tlen.png").convert_alpha(), (200, 80))
    tlen_pust = pygame.transform.scale(pygame.image.load("Images/tlen_pusty.png").convert_alpha(), (200, 80))
    diver_icon = pygame.transform.scale(pygame.image.load("Images/plywak0.png").convert_alpha(), (50, 30))

    # 3. EKRAN STARTOWY
    while True:

        # --- EKRAN STARTOWY / MENU ---
        start_screen = StartScreen()
        menu_active = True

        while menu_active:
            start_screen.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # START ROZGRYWKI
                    if start_screen.start_rect.collidepoint(event.pos):
                        menu_active = False

                    # WYJŚCIE
                    if start_screen.quit_rect.collidepoint(event.pos):
                        pygame.quit();
                        sys.exit()

                    # HIGHSCORE
                    if start_screen.highscore_rect.collidepoint(event.pos):
                        current_top = score_manager.get_high_score(0)
                        hs_screen = HighscoreScreen(current_top)

                        viewing_hs = True
                        while viewing_hs:
                            hs_screen.draw(screen)
                            pygame.display.flip()
                            for hs_event in pygame.event.get():
                                if hs_event.type == pygame.QUIT:
                                    pygame.quit();
                                    sys.exit()
                                if hs_event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                                    viewing_hs = False

        # 4. KONFIGURACJA POZIOMÓW
        levels = [
            LevelConfig(1, 2500, "Background_sea.png"),
            LevelConfig(2, 1200, "Background_dark_sea.png")
        ]
        current_lvl_idx = 0

        # 5. PRE-LOADING ZASOBÓW
        tlen_full = pygame.transform.scale(pygame.image.load("Images/tlen.png").convert_alpha(), (200, 80))
        tlen_pust = pygame.transform.scale(pygame.image.load("Images/tlen_pusty.png").convert_alpha(), (200, 80))
        diver_icon = pygame.transform.scale(pygame.image.load("Images/plywak0.png").convert_alpha(), (50, 30))

        # 6. ŁADOWANIE GRAFIKI LVL2
        level_2_banner = pygame.image.load("Images/level_2.png").convert_alpha()
        level_2_banner = pygame.transform.scale(level_2_banner, (400, 200))
        level_banner_rect = level_2_banner.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        # 7. PRE-LOADING TŁA W ZALEŻNOŚĆ OD LVL
        level_backgrounds = []
        for lvl in levels:
            try:
                img = pygame.image.load(os.path.join("Images", lvl.bg_file)).convert()
                level_backgrounds.append(pygame.transform.scale(img, (WIDTH, HEIGHT)))
            except:
                dummy_bg = pygame.Surface((WIDTH, HEIGHT))
                dummy_bg.fill((0, 50, 100))
                level_backgrounds.append(dummy_bg)

        # INICJALIZACJA GRUP OBIEKTÓW
        player = Player()
        all_sprites = pygame.sprite.Group(player)
        fishes, enemies_group, enemy_bullets, divers_group = [pygame.sprite.Group() for _ in range(4)]

        last_spawn_time = last_enemy_spawn = last_diver_spawn = pygame.time.get_ticks()

        # 8. PĘTLA WEWNĘTRZNA
        running = True
        while running:
            lvl = levels[current_lvl_idx]
            background = level_backgrounds[current_lvl_idx]
            current_time = pygame.time.get_ticks()

            # --- OBSŁUGA ZDARZEŃ I WEJŚCIA UŻYTKOWNIKA ---

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.shoot()
                    if shoot_sound: shoot_sound.play()

            # --- SPAWNOWANIE ---

            if current_time - last_enemy_spawn > lvl.spawn_delay:
                prob = random.random()

                if prob < 0.15:  # 15% szansy na dużego wroga
                    new_enemy = BigAggressive()
                elif prob < 0.50:  # 35% szansy na średniego (0.50 - 0.15)
                    new_enemy = MediumAggressive()
                else:  # 50% szansy na małego
                    new_enemy = SmallAggressive()

                all_sprites.add(new_enemy)
                enemies_group.add(new_enemy)
                last_enemy_spawn = current_time

            if current_time - last_spawn_time > 4000:
                f = GoldenFish(); all_sprites.add(f); fishes.add(f)
                last_spawn_time = current_time

            if current_time - last_diver_spawn > 15000:
                d = Diver(WIDTH + 50, random.randint(WATER_LINE + 50, HEIGHT - 50))
                all_sprites.add(d); divers_group.add(d)
                last_diver_spawn = current_time

            # --- AKTUALIZACJA ---

            player.update()
            player.bullets.update()
            fishes.update()
            enemy_bullets.update()
            divers_group.update()

            # --- PODEJMOWANIE DECYZJI O STRZALE ---

            for enemy in enemies_group:
                if enemy.update():
                    direction = 1 if enemy.facing == "right" else -1
                    spawn_x = enemy.rect.right if direction == 1 else enemy.rect.left
                    bullet = EnemyBullet(spawn_x, enemy.rect.centery, direction)
                    all_sprites.add(bullet); enemy_bullets.add(bullet)

            # --- KOLIZJE ---

            if pygame.sprite.spritecollide(player, divers_group, True):
                player.saved_divers += 1; player.score += 50
                player.oxygen = min(100, player.oxygen + 15)

            if pygame.sprite.spritecollide(player, fishes, True):
                player.score += 25; player.oxygen = min(100, player.oxygen + 10)

            collided_enemies = pygame.sprite.spritecollide(player, enemies_group, True)
            for enemy in collided_enemies:
                if hasattr(enemy, 'oxygen_damage'):
                    player.oxygen -= enemy.oxygen_damage
                else:
                    player.oxygen -= 20

            if pygame.sprite.spritecollide(player, enemy_bullets, True):
                player.oxygen -= 20

            hits = pygame.sprite.groupcollide(enemies_group, player.bullets, False, True)
            for enemy in hits:
                enemy.hp -= 1
                if enemy.hp <= 0:
                    player.score += getattr(enemy, 'score_value', 20)
                    enemy.kill()

            # --- LOGIKA POZIOMÓW ---

            if player.saved_divers >= 5:
                if current_lvl_idx < len(levels) - 1:
                    current_lvl_idx += 1
                    player.saved_divers = 0
                    player.oxygen = 100
                    enemies_group.empty()
                    enemy_bullets.empty()
                    fishes.empty()
                    divers_group.empty()
                    player.rect.center = (WIDTH // 2, HEIGHT // 2)

                    all_sprites.empty()
                    all_sprites.add(player)

                    screen.fill(BLACK)
                    screen.blit(level_2_banner, level_banner_rect)
                    pygame.display.flip()
                    pygame.time.delay(1500)
                else:
                    score_manager.check_and_save(player.score)
                    WinScreen(player.score).draw(screen)
                    pygame.display.flip(); pygame.time.delay(5000); running = False

            if player.oxygen <= 20:
                score_manager.check_and_save(player.score)
                LoseScreen(player.score).draw(screen)
                pygame.display.flip(); pygame.time.delay(5000); running = False

            # --- RYSOWANIE ---

            screen.blit(background, (0, 0))
            all_sprites.draw(screen)
            player.bullets.draw(screen)
            draw_ui(screen, player, tlen_full, tlen_pust, diver_icon, lvl.number)

            pygame.display.flip()
            clock.tick(FPS)

    main()