import asyncio
import math
import random

import pygame
from pygame import mixer

# Screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance < 10


def draw_player(screen, img_player, x, y):
    screen.blit(img_player, (x, y))


def draw_enemy(screen, img_enemy_list, index, x, y):
    screen.blit(img_enemy_list[index], (x, y))


def draw_bullet(screen, img_bullet, x, y):
    screen.blit(img_bullet, (x + 16, y + 10))


def draw_score(screen, font, score, x, y):
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))


def draw_game_over(screen, font):
    text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(text, (200, 200))


async def main():
    pygame.init()

    # Mixer can fail on web, so guard it
    sound_ok = True
    try:
        mixer.init()
    except pygame.error:
        sound_ok = False

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invasion")

    # Load assets
    icon = pygame.image.load("assets/ufo.png")
    pygame.display.set_icon(icon)

    background = pygame.image.load("assets/Background.jpg")

    img_player_full = pygame.image.load("assets/rocket.png")
    original_width = img_player_full.get_width()
    original_height = img_player_full.get_height()
    img_player = pygame.transform.scale(
        img_player_full,
        (int(original_width * 0.2), int(original_height * 0.2)),
    )

    # Enemies
    img_enemy = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    number_of_enemies = 10

    for _ in range(number_of_enemies):
        img_enemy.append(pygame.image.load("assets/enemy.png"))
        enemy_x.append(random.randint(0, 715))
        enemy_y.append(random.randint(50, 200))
        enemy_x_change.append(0.5)
        enemy_y_change.append(20)

    img_bullet = pygame.image.load("assets/bullet.png")

    # Fonts (None = default font, avoids needing a .ttf file)
    score_font = pygame.font.Font(None, 32)
    end_font = pygame.font.Font(None, 40)

    # Music
    if sound_ok:
        try:
            mixer.music.load("assets/background_music.mp3")
            mixer.music.set_volume(0.3)
            mixer.music.play(-1)
        except pygame.error:
            pass  # if music fails, just skip it

    # Game state
    player_x = 349
    player_y = 475
    player_x_change = 0

    bullet_x = 0
    bullet_y = 470
    bullet_y_change = 1.5
    visible_bullet = False

    score = 0
    game_over = False
    running = True

    clock = pygame.time.Clock()

    while running:
        # Draw background
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -1
                elif event.key == pygame.K_RIGHT:
                    player_x_change = 1
                elif event.key == pygame.K_SPACE:
                    if not visible_bullet:
                        bullet_x = player_x
                        visible_bullet = True
                        if sound_ok:
                            try:
                                bullet_sound = mixer.Sound("assets/shot.mp3")
                                bullet_sound.play()
                            except pygame.error:
                                pass

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player_x_change = 0

        # Bullet movement
        if bullet_y <= -64:
            bullet_y = 470
            visible_bullet = False
        if visible_bullet:
            draw_bullet(screen, img_bullet, bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        # Player movement
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 715:
            player_x = 715

        # Enemies logic
        for i in range(number_of_enemies):
            if enemy_y[i] > 400:
                game_over = True

            enemy_x[i] += enemy_x_change[i]

            if enemy_x[i] <= 0:
                enemy_x_change[i] = 0.75
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 715:
                enemy_x_change[i] = -0.75
                enemy_y[i] += enemy_y_change[i]

            # Collision
            if visible_bullet and is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                bullet_y = 470
                visible_bullet = False
                score += 1

                if sound_ok:
                    try:
                        collision_sound = mixer.Sound("assets/punch.mp3")
                        collision_sound.play()
                    except pygame.error:
                        pass

                enemy_x[i] = random.randint(0, 715)
                enemy_y[i] = random.randint(50, 200)

            draw_enemy(screen, img_enemy, i, enemy_x[i], enemy_y[i])

        draw_player(screen, img_player, player_x, player_y)
        draw_score(screen, score_font, score, 10, 10)

        if game_over:
            draw_game_over(screen, end_font)

        pygame.display.flip()
        clock.tick(60)

        # Critical for pygbag: yield back to browser
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
