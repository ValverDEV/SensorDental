# INITIALIZE PROGRAM

from turtle import back
import pygame
import Tooth_btn
from Tooth_btn import Tooth
from render import Render

# Initialize pygame
pygame.init()

Render = Render()


screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('./assets/bg.png')

# Create Teeth buttons
teeth = Tooth_btn.create_teeth()

# Draw Teeth
green_cir = pygame.image.load('./assets/green.png')
grey_cir = pygame.image.load('./assets/grey.png')
red_cir = pygame.image.load('./assets/red.png')
yellow_cir = pygame.image.load('./assets/yellow.png')

sgreen_cir = pygame.transform.scale(green_cir, (30, 30))
sgrey_cir = pygame.transform.scale(grey_cir, (30, 30))
sred_cir = pygame.transform.scale(red_cir, (30, 30))
syellow_cir = pygame.transform.scale(yellow_cir, (30, 30))

colors = {
    'green': {
        'n': green_cir,
        's': sgreen_cir
    },
    'grey': {
        'n': grey_cir,
        's': sgrey_cir
    },
    'red': {
        'n': red_cir,
        's': sred_cir
    },
    'yellow': {
        'n': yellow_cir,
        's': syellow_cir
    }
}


def draw_teeth():
    for tooth in teeth:
        color = tooth.color
        size = tooth.size
        pos = tooth.position
        screen.blit(colors[color][size], pos)


def count_measured():
    count = 0
    for tooth in teeth:
        if tooth.temp:
            count += 1
    return count
# ---------------------------------------------------

# MAIN


run = True
while run:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for tooth in teeth:
                if tooth.check_click(mouse_pos):
                    Render.active = tooth
                    if tooth.temp:
                        Render.init_measured()
                        Render.state = 'active-measured'
                    else:
                        Render.init_not_measured()
                        Render.state = 'active-not-measured'

                    break
            Render.clicked(mouse_pos)

        else:
            Render.isClick = False

    draw_teeth()

    Render.render(screen)

    pygame.display.update()
