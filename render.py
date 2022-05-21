import pygame
from button import Button
from statistics import mean, stdev

pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 32)
black = (0, 0, 0)
red = (255, 0, 0)


class Render:

    # Constructor
    def __init__(self, screen):
        self.screen = screen
        self.state = 'inactive'
        try:
            from serial_py import serial_get_temp
        except:
            self.state = 'serial_error_init'
            self.render()
        self.active = None
        self.buttons = []
        self.isClick = False
        self.measured = 0
        self.needTemps = False
        self.mean = None
        self.std = None

    # Casos de render

    def render(self):

        # Caso inicial
        if self.state == 'inactive':
            if not self.mean:
                text = font.render(
                    'Da click en un diente para medir', True, black)
                self.screen.blit(text, (0, 600-32))
            else:
                text_mean = font.render(
                    f'Mean: {round(self.mean, 3)}', True, black)
                self.screen.blit(text_mean, (0, 600 - 100))
                text_std = font.render(
                    f'Std. Var: {round(self.std, 3)}', True, black)
                self.screen.blit(text_std, (0, 600 - 50))

        # Diente seleccionado, sin medir
        if self.state == 'active-not-measured':
            text = font.render(self.active.name, True, black)
            textRect = text.get_rect(center=(400, 400))

            btn = self.buttons[0]

            self.screen.blit(text, textRect)
            self.screen.blit(btn.btn, btn.pos)

        # Diente seleccionado, midiendo
        if self.state == 'active-measuring':
            # newTemp = 32 + randint(-1, 1) + randint(0, 99)/100
            current_ticks = pygame.time.get_ticks()
            if current_ticks >= self.tracker + 1000:
                self.newTemp = self.read_temp()
                if self.newTemp:
                    self.active.measuring.append(self.newTemp)
                    self.tracker = pygame.time.get_ticks()

            temp = font.render(f'Temperatura: {self.newTemp}', True, black)
            tempRect = temp.get_rect(center=(230, 450))
            name = font.render(self.active.name, True, black)
            nameRect = name.get_rect(center=(230, 490))
            self.screen.blit(temp, tempRect)
            self.screen.blit(name, nameRect)

            btn = self.buttons[0]
            self.screen.blit(btn.btn, btn.pos)

            if len(self.active.measuring) >= 5:
                self.measured += 1
                self.init_measured()
                self.state = 'active-measured'

        if self.state == 'active-measured':
            temp = font.render(f'Temperatura: {self.active.temp}', True, black)
            tempRect = temp.get_rect(center=(230, 450))
            name = font.render(self.active.name, True, black)
            nameRect = name.get_rect(center=(230, 490))

            self.screen.blit(temp, tempRect)
            self.screen.blit(name, nameRect)

            for btn in self.buttons:
                self.screen.blit(btn.btn, btn.pos)

        if self.state == 'serial_error_init':
            text = font.render(
                'SENSOR NO CONECTADO', True, (255, 255, 255))
            self.screen.blit(text, (0, 0))
            self.quit()

    def init_not_measured(self):
        self.buttons = []
        btn = Button('Medir', (400, 470))
        self.buttons.append(btn)

    def init_measuring(self):
        self.buttons = []
        self.active.measuring = []
        btn = Button('Detener', (580, 470))
        self.buttons.append(btn)
        self.tracker = pygame.time.get_ticks()
        self.newTemp = self.read_temp()

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

            if temps[i] < m-std*2 or temps[i] > m+std*2:  # danger
                teeth[i].color = 'red'

            elif temps[i] < m-std or temps[i] > m+std:  # warning
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

    def read_temp(self):
        try:
            temp = serial_get_temp()
            return temp
        except:
            text = font.render(
                'NO SE ENCONTRÓ EL SENSOR', True, red)
            self.screen.blit(text, (0, 0))
            self.quit()

    def quit(self):
        pygame.display.update()
        from sys import exit
        from time import sleep
        sleep(5)
        exit()
