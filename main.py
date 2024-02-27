import pygame
import random

#Initialise pgame
pygame.init()

#Create the screen
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Space Invasion")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#player
img_player1 = pygame.image.load("rocket.png")
original_width = img_player1.get_width()
original_height = img_player1.get_height()
img_player = pygame.transform.scale(img_player1,(int(original_width * 0.2),int(original_height * 0.2)))
player_x = 349
player_y = 475
player_x_change = 0
# print to the concole the scaled down width and height of the player
#print(int(original_width * 0.2),int(original_height * 0.2))

#Enemy variables
img_enemy = pygame.image.load("enemy.png")
enemy_x = random.randint(0,715)
enemy_y = random.randint(50,200)
enemy_x_change = 0


# Create player
def player(x,y):
    screen.blit(img_player, (x,y))

# Create enemy
def enemy(x,y):
    screen.blit(img_enemy, (x,y))   

# Game loop
running = True
while running:
    # Set screen color
    screen.fill((200,144,228))
    
    
    for event in pygame.event.get():
        # Close event
        if event.type == pygame.QUIT:
            running = False

        # Press arrow key event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:
                 player_x_change = 0.3
        # Release arrow key event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                 player_x_change = 0

    # Modify location
    player_x += player_x_change

    # Set Limit boundaries
    if player_x <= 0:
        player_x = 0
    elif player_x >= 715:
        player_x = 715

    player(player_x,player_y)
    enemy(enemy_x,enemy_y)


    # Update
    pygame.display.update()
    