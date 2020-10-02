import pygame
import math
import random
from pygame import mixer

# initialise pygame
pygame.init()

# creating window, set_mode(should be under tuple.)
screen = pygame.display.set_mode((800, 600))

#background image
background = pygame.image.load('background.png')

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Adding Title and Icon

title = pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('rocket.png')
pygame.display.set_icon(icon)

# PLAYER
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# ENEMY

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemy = 6

for i in range(number_of_enemy):

    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# BULLET
#ready -> you cannot see bullet on the screen
#Fire -> bullets will be visible on the screen
bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
fontX = 10
fontY = 10

#GAME OVER
over_font = pygame.font.Font("freesansbold.ttf", 64)
overX = 50
overY = 50

def game_over_text(overX, overY):
    over_text = font.render("GAME OVER",True, (255,255,255))
    screen.blit(over_text, (overX, overY))

def show_font(fontX,fontY):
    score = over_font.render("Score:" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (fontX, fontY))

def player(playerX, playerY):
    # blit() is used to draw the player image over the screen
    screen.blit(playerimg, (playerX, playerY))


def enemy(enemyX, enemyY, i):
    screen.blit(enemyimg[i], (enemyX, enemyY))

def fire_bullet(bulletX, bulletY):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(bulletX+15, bulletY-15))

# making a Collision function to get  distance between enemy and the bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + (math.pow(enemyY-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Adding GAMELOOP

running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # Get the current x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(number_of_enemy):

        if enemyY[i] > 440:
            for j in range(number_of_enemy):
                enemyY[j] = 2000

            game_over_text(overX, overY)
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explode = mixer.Sound("explosion.wav")
            explode.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_font(fontX, fontY)
    player(playerX, playerY)
    pygame.display.update()