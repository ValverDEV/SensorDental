import pygame
from button import Button
from statistics import mean, stdev

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
        self.state = 'inactive'
        self.active = None
        self.buttons = []
        self.isClick = False
        self.measured = 0
        self.needTemps = False
        self.mean = None
        self.std = None

    # Casos de render
    def render(self, screen):

        # Caso inicial
        if self.state == 'inactive':
            if not self.mean:
                text = font.render(
                    'Da click en un diente para medir', True, black)
                screen.blit(text, (0, 600-32))
            else:
                text_mean = font.render(f'Mean: {self.mean}', True, black)
                screen.blit(text_mean, (0, 600 - 100))
                text_std = font.render(f'Std. Var: {self.std}', True, black)
                screen.blit(text_std, (0, 600 - 50))

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

            if len(self.active.measuring) >= 1:
                self.measured += 1
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
        btn = Button('Medir', (400, 470))
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
            self.active.color = 'blue'
        btn_rep = Button('Repetir', (520, 460), 'yellow')
        btn_del = Button('Borrar', (680, 460), 'red')
        self.buttons = []
        self.buttons.append(btn_rep)
        self.buttons.append(btn_del)

        if self.measured >= 3:
            btn_an = Button('Analizar', (600, 550))
            self.buttons.append(btn_an)

    def analyze(self, teeth):
        temps = [tooth.temp for tooth in teeth]
        m = mean(temps)
        std = stdev(temps)

        # check tooth
        for i in range(len(temps)):

            if temps[i] < m-std or temps[i] > m+std:  # danger
                teeth[i].color = 'red'

            elif temps[i] < m-std/2 or temps[i] > m+std/2:  # warning
                teeth[i].color = 'yellow'
            else:  # normal
                teeth[i].color = 'green'

        self.mean = m
        self.std = std
        self.needTemps = False
        self.state = 'inactive'

    def clicked(self, mouse_pos):

        if self.state == 'active-not-measured':
            btn = self.buttons[0]
            if btn.check_click(mouse_pos):
                self.init_measuring()
                self.state = 'active-measuring'

            else:
                self.state = 'inactive'

        if self.state == 'active-measuring':
            btn = self.buttons[0]
            if btn.check_click(mouse_pos):
                self.init_not_measured()
                self.state = 'active-not-measured'

        if self.state == 'active-measured':
            btn_rep = self.buttons[0]
            btn_del = self.buttons[1]
            btn_an = None

            if len(self.buttons) == 3:
                btn_an = self.buttons[2]

            if btn_rep.check_click(mouse_pos):
                self.active.temp = 0.0
                self.active.color = 'grey'
                self.measured -= 1
                self.init_measuring()
                self.state = 'active-measuring'

            elif btn_del.check_click(mouse_pos):
                self.active.temp = 0.0
                self.active.color = 'grey'
                self.measured -= 1
                self.state = 'inactive'

            elif btn_an:
                if btn_an.check_click(mouse_pos):
                    self.needTemps = True

                else:
                    self.state = 'inactive'
