import pygame
from button import Button
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

    # Casos de render
    def render(self, screen):

        # Caso inicial
        if self.state == 'start':
            text = font.render('Da click en un diente para medir', True, black)
            screen.blit(text, (0, 600-32))

        # Diente seleccionado, sin medir (inicia)
        if self.state == 'active-not-measured-start':
            btn = Button('Iniciar', (400, 470))

            screen.blit(btn.btn, btn.pos)

            self.buttons.append(btn)
            self.state = 'active-not-measured'

        # Diente seleccionado, sin medir (inicia)
        if self.state == 'active-not-measured':
            text = font.render('Diente', True, black)
            textRect = text.get_rect(center=(400, 400))

            btn = self.buttons[0]

            if self.isClick:

                for btn in self.buttons:
                    mouse_pos = pygame.mouse.get_pos()
                    if btn.check_click(mouse_pos):
                        self.state = 'active-measuring'

            screen.blit(text, textRect)
            screen.blit(btn.btn, btn.pos)

        # Diente seleccionado, midiendo
        if self.state == 'active-measuring':
            print('measuring')
