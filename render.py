import pygame
pygame.font.init()

font = pygame.font.Font(pygame.font.get_default_font(), 32)
black = (0, 0, 0)


class Render:

    def __init__(self):
        self.state = 'start'
        self.active = None

    def render(self, screen):

        if self.state == 'start':
            text = font.render('Da click en un diente para medir', True, black)
            screen.blit(text, (0, 600-32))

        if self.state == 'active-not-measured':
            text = font.render('Diente', True, black)
            textRect = text.get_rect(center=(400, 400))
            screen.blit(text, textRect)
