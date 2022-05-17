import pygame
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 32)
black = (0, 0, 0)
white = (255, 255, 255)
pad = 20
dpad = pad*2


class Button:

    def __init__(self, text, center):
        self.text = font.render(text, True, black, white)
        self.textPos = self.text.get_rect(center=center)
        w, h = self.textPos.width + dpad, self.textPos.height + dpad
        self.btn = pygame.Surface((w, h))
        self.btn.fill(white)
        self.btn.blit(self.text, (pad, pad))
        self.pos = self.btn.get_rect(center = center)
        self.x1, self.y1 = self.pos.topleft[0], self.pos.topleft[1]
        self.x2, self.y2 = self.pos.bottomright[0], self.pos.bottomright[1]
    
    def check_click(self, click):
        x, y = click[0], click[1]
        if (x >= self.x1 and x <= self.x2) and (y >= self.y1 and y <= self.y2):
            return True
        return False
