from matplotlib.pyplot import text
import pygame
from pygame import mixer
from random import randint
from math import sqrt

# initializae pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('./assets/background.png')

# Background sound
mixer.music.load('./assets/background.wav')
mixer.music.play(-1)

# Sounds
bullet_Sound = mixer.Sound('./assets/laser.wav')
explosion_sound = mixer.Sound('./assets/explosion.wav')

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('./assets/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('./assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('./assets/enemy.png'))
    enemyX.append(randint(0, 750))
    enemyY.append(randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('./assets/bullet.png')
bulletX = 0
bulletY = playerY
bulletY_change = 10
bullet_state = 'ready'

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def player():
    screen.blit(playerImg, (playerX, playerY))


def enemy(i):
    screen.blit(enemyImg[i], (enemyX[i], enemyY[i]))


def fire_bullet():
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (bulletX, bulletY + 10))


def isCollission(enemyX, enemyY, bulletX, bulletY):
    distance = sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:
        return True
    return False


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    over_text = over_font.render('Game Over', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_Sound.play()
                    bulletX = playerX + 16
                    fire_bullet()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0 or enemyX[i] >= 736:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        collission = isCollission(enemyX[i], enemyY[i], bulletX, bulletY)
        if collission:
            explosion_sound.play()
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = randint(0, 750)
            enemyY[i] = randint(50, 150)

        enemy(i)

    # Bullet Movement
    if bulletY <= 0:

        bulletY = playerY
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fire_bullet()
        bulletY -= bulletY_change

    player()
    show_score(textX, testY)

    pygame.display.update()
