import pygame
import random
import math
from pygame import mixer

# Initialise pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("assets/ufo.png")
pygame.display.set_icon(icon)
background = pygame.image.load("assets/Background.jpg")

# Add music
mixer.music.load('assets/background_music.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Player
img_player1 = pygame.image.load("assets/rocket.png")
original_width = img_player1.get_width()
original_height = img_player1.get_height()
img_player = pygame.transform.scale(
    img_player1,
    (int(original_width * 0.2), int(original_height * 0.2))
)
player_x = 349
player_y = 475
player_x_change = 0

# Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 10

for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load("assets/enemy.png"))
    enemy_x.append(random.randint(0, 715))
    enemy_y.append(random.randint(50, 200))
    enemy_x_change.append(0.5)
    enemy_y_change.append(20)

# Bullet variables
img_bullet = pygame.image.load("assets/bullet.png")
bullet_x = 0
bullet_y = 470
bullet_y_change = 1.5
visible_bullet = False

# Score
score = 0
font_style = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# End of game text
end_font = pygame.font.Font('freesansbold.ttf', 40)


def final_text():
    my_final_text = end_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(my_final_text, (200, 200))


# Show score function
def show_score(x, y):
    text = font_style.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (x, y))


# Create player
def player(x, y):
    screen.blit(img_player, (x, y))


# Create enemy
def enemy(x, y, en):
    screen.blit(img_enemy[en], (x, y))


# Shoot bullet
def shoot_bullet(x, y):
    global visible_bullet
    visible_bullet = True
    screen.blit(img_bullet, (x + 16, y + 10))


# Detect collision function
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(
        (enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2
    )
    return distance < 27  # tweak as needed


def main():
    global player_x, player_x_change, bullet_x, bullet_y, visible_bullet, score

    running = True
    game_over = False

    while running:
        # Draw background
        screen.blit(background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            # Close event
            if event.type == pygame.QUIT:
                running = False

            # Key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -1
                if event.key == pygame.K_RIGHT:
                    player_x_change = 1
                if event.key == pygame.K_SPACE:
                    bullet_sound = mixer.Sound('assets/shot.mp3')
                    bullet_sound.play()
                    if not visible_bullet:
                        bullet_x = player_x
                        shoot_bullet(bullet_x, bullet_y)

            # Key released
            if event.type == pygame.KEYUP:
                # check if LEFT or RIGHT is released
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player_x_change = 0

        # Bullet movement
        if bullet_y <= -64:
            bullet_y = 470
            visible_bullet = False

        if visible_bullet:
            shoot_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        # Player movement
        player_x += player_x_change

        # Player boundaries
        if player_x <= 0:
            player_x = 0
        elif player_x >= 715:
            player_x = 715

        # Enemy movement
        for enem in range(number_of_enemies):
            # End of game condition
            if enemy_y[enem] > 400:
                game_over = True
                break

            enemy_x[enem] += enemy_x_change[enem]

            # Enemy boundaries and descent
            if enemy_x[enem] <= 0:
                enemy_x_change[enem] = 0.75
                enemy_y[enem] += enemy_y_change[enem]
            elif enemy_x[enem] >= 715:
                enemy_x_change[enem] = -0.75
                enemy_y[enem] += enemy_y_change[enem]

            # Collision
            if is_collision(enemy_x[enem], enemy_y[enem], bullet_x, bullet_y):
                collision_sound = mixer.Sound('assets/punch.mp3')
                collision_sound.play()
                bullet_y = 470
                visible_bullet = False
                score += 1
                enemy_x[enem] = random.randint(0, 715)
                enemy_y[enem] = random.randint(50, 200)

            enemy(enemy_x[enem], enemy_y[enem], enem)

        # Draw player
        player(player_x, player_y)

        # Show score
        show_score(text_x, text_y)

        # Show final text when game is over
        if game_over:
            final_text()
            pygame.display.update()
            return  # exit main(), then quit pygame

        # Update screen
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
