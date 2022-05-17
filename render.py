import pygame
from button import Button
from statistics import mean

# borrar
from random import randint
from time import sleep

###################
pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 32)
black = (0, 0, 0)


class Render:

    # Constructor
    def __init__(self):
        self.state = 'start'
        self.active = None
        self.buttons = []
        self.isClick = False
        self.measured = 0

    # Casos de render
    def render(self, screen):

        # Caso inicial
        if self.state == 'start':
            text = font.render('Da click en un diente para medir', True, black)
            screen.blit(text, (0, 600-32))

        # Diente seleccionado, sin medir
        if self.state == 'active-not-measured':
            text = font.render(self.active.name, True, black)
            textRect = text.get_rect(center=(400, 400))

            btn = self.buttons[0]

            screen.blit(text, textRect)
            screen.blit(btn.btn, btn.pos)

        # Diente seleccionado, midiendo
        if self.state == 'active-measuring':
            newTemp = 32 + randint(-1, 1) + randint(0, 99)/100
            self.active.measuring.append(newTemp)

            temp = font.render(f'Temperatura: {newTemp}', True, black)
            tempRect = temp.get_rect(center=(230, 450))
            name = font.render(self.active.name, True, black)
            nameRect = name.get_rect(center=(230, 490))
            screen.blit(temp, tempRect)
            screen.blit(name, nameRect)

            btn = self.buttons[0]
            screen.blit(btn.btn, btn.pos)

            sleep(1)

            if len(self.active.measuring) >= 5:
                self.init_measured()
                self.state = 'active-measured'

        if self.state == 'active-measured':
            temp = font.render(f'Temperatura: {self.active.temp}', True, black)
            tempRect = temp.get_rect(center=(230, 450))
            name = font.render(self.active.name, True, black)
            nameRect = name.get_rect(center=(230, 490))

            screen.blit(temp, tempRect)
            screen.blit(name, nameRect)

            for btn in self.buttons:
                screen.blit(btn.btn, btn.pos)

    def init_not_measured(self):
        self.buttons = []
        btn = Button('Iniciar', (400, 470))
        self.buttons.append(btn)

    def init_measuring(self):
        self.buttons = []
        self.active.measuring = []
        btn = Button('Detener', (580, 470))
        self.buttons.append(btn)

    def init_measured(self):
        if not self.active.temp:
            self.active.temp = mean(self.active.measuring)
            self.active.measuring = []
            self.active.color = 'green'
        btn_rep = Button('Repetir', (520, 470), 'yellow')
        btn_del = Button('Borrar', (680, 470), 'red')
        self.buttons = []
        self.buttons.append(btn_rep)
        self.buttons.append(btn_del)

    def clicked(self, mouse_pos):

        if self.state == 'active-not-measured':
            btn = self.buttons[0]
            if btn.check_click(mouse_pos):
                self.init_measuring()
                self.state = 'active-measuring'

        if self.state == 'active-measuring':
            btn = self.buttons[0]
            if btn.check_click(mouse_pos):
                self.init_not_measured()
                self.state = 'active-not-measured'

        if self.state == 'active-measured':
            btn_rep = self.buttons[0]
            btn_del = self.buttons[1]

            if btn_rep.check_click(mouse_pos):
                self.active.temp = 0.0
                self.active.color = 'grey'
                self.init_measuring()
                self.state = 'active-measuring'

            if btn_del.check_click(mouse_pos):
                self.active.temp = 0.0
                self.active.color = 'grey'
                self.state = 'start'
