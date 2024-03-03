import pygame
import random
import math
from pygame import mixer

#Initialise pgame
pygame.init()

#Create the screen
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
background = pygame.image.load("Background.jpg")

# add music
mixer.music.load('background_music.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

#player
img_player1 = pygame.image.load("rocket.png")
original_width = img_player1.get_width()
original_height = img_player1.get_height()
img_player = pygame.transform.scale(img_player1,(int(original_width * 0.2),int(original_height * 0.2)))
player_x = 349
player_y = 475
player_x_change = 0
# print to the concole the scaled down width and height of the player (Used when the size and dimension of the image)
#print(int(original_width * 0.2),int(original_height * 0.2))

#Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 10

#Enemy variables
for e in range(number_of_enemies):
    img_enemy.append(pygame.image.load("enemy.png")) 
    enemy_x.append(random.randint(0,715))
    enemy_y.append(random.randint(50,200))
    enemy_x_change.append(0.5)
    enemy_y_change.append(20)

# Bullet variables
img_bullet = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 470
bullet_y_change = 1.5
visible_bullet = False

# Score
score = 0
font_style = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Show score function
def show_score(x,y):
     text = font_style.render(f'Score: {score}',True, (255,255,255))
     screen.blit(text, (x,y))

# Create player
def player(x,y):
    screen.blit(img_player, (x,y))

# Create enemy
def enemy(x,y,en):
    screen.blit(img_enemy[en], (x,y))   

# Shoot bullet
def shoot_bullet(x,y):
    global visible_bullet
    visible_bullet = True
    screen.blit(img_bullet,(x+16,y+10))

# Detect collision function
def is_collision(x_1,x_2,y_1,y_2):
    distance = math.sqrt((math.pow((x_2 - x_1),2) + math.pow((y_2 - y_1),2)))
    if distance < 10:
        return True
    else :
        return False
    
# Game loop
running = True
while running:
    # Set screen color
    # screen.fill((200,100,50))
    screen.blit(background,(0,0))
    
    
    for event in pygame.event.get():
        # Close event
        if event.type == pygame.QUIT:
            running = False

        # Press keys event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                 player_x_change = 1
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('shot.mp3')
                bullet_sound.play()
                if visible_bullet == False:
                    bullet_x = player_x
                    shoot_bullet(bullet_x, bullet_y)

        # Release arrow key event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                 player_x_change = 0

    # Bullets movement 
    if bullet_y <= -64:
        bullet_y = 470
        visible_bullet = False
    if visible_bullet == True :
        shoot_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_y_change

    # Modify location
    player_x += player_x_change

    # Set Limit boundaries
    if player_x <= 0:
        player_x = 0
    elif player_x >= 715:
        player_x = 715

     #Modify enemy location
    for enem in range(number_of_enemies):   
        enemy_x[enem] += enemy_x_change[enem]
        # Set Limit boundaries
        if enemy_x[enem] <= 0:
            enemy_x_change[enem] = 0.75
            enemy_y[enem] += enemy_y_change[enem]
        elif enemy_x[enem] >= 715:
            enemy_x_change[enem] = -0.75
            enemy_y[enem] += enemy_y_change[enem]  

        #Collision
        collision = is_collision(enemy_x[enem],enemy_y[enem],bullet_x,bullet_y)
        if collision:
            bullet_y = 470
            visible_bullet = False
            score += 1
            enemy_x[enem] = random.randint(0,715)
            enemy_y[enem] = random.randint(50,200)
        
        enemy(enemy_x[enem],enemy_y[enem], enem)
        
    player(player_x,player_y)

    show_score(text_x,text_y)
    
    # Update
    pygame.display.update()
    