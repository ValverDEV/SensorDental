from itertools import tee
from re import L
import pygame

teeth_pos = [
    (115, 131), (115, 167), (124, 204), (138, 239), (158, 270),
    (177, 292), (195, 303), (219, 309), (243, 310), (264, 303),
    (284, 291), (302, 267), (323, 237), (336, 203), (345, 167),
    (345, 128), (468, 305), (465, 270), (472, 235), (485, 204),
    (500, 175), (515, 149), (537, 129), (567, 116), (600, 118),
    (631, 128), (649, 150), (668, 177), (682, 202), (696, 235),
    (702, 268), (699, 304)
]

names = [
    'Muela del juicio',
    'Segundo Molar',
    'Primer Molar',
    'Segundo Premolar',
    'Primer Premolar',
    'Canino',
    'Incisivo Lateral',
    'Incisivo Central',
    'Incisivo Central',
    'Incisivo Lateral',
    'Canino',
    'Primer Premolar',
    'Segundo Premolar',
    'Primer Molar',
    'Segundo Molar',
    'Muela del juicio',
    'Muela del juicio',
    'Segundo Molar',
    'Primer Molar',
    'Segundo Premolar',
    'Primer Premolar',
    'Canino',
    'Incisivo Lateral',
    'Incisivo Central',
    'Incisivo Central',
    'Incisivo Lateral',
    'Canino',
    'Primer Premolar',
    'Segundo Premolar',
    'Primer Molar',
    'Segundo Molar',
    'Muela del juicio',
]

sizes = ['n' if i < 5 or i > 10 else 's' for i in range(len(teeth_pos))]


def create_teeth():
    teeth = []
    for i in range(len(teeth_pos)):
        teeth.append(Tooth(names[i], teeth_pos[i], sizes[i]))
    return teeth


class Tooth:

    def create_limits(self):
        if self.size == 'n':
            self.x1 = self.position[0]
            self.x2 = self.position[0] + 40
            self.y1 = self.position[1]
            self.y2 = self.position[1] + 40
        else:
            self.x1 = self.position[0]
            self.x2 = self.position[0] + 30
            self.y1 = self.position[1]
            self.y2 = self.position[1] + 30

    def __init__(self, name, position, size):
        self.name = name
        self.color = 'grey'
        self.temp = 0.0
        self.done = False
        self.size = size
        self.measuring = []

        if size == 'n':
            self.position = (position[0] - 20, position[1] - 20)
        else:
            self.position = (position[0] - 15, position[1] - 15)

        self.create_limits()

    def check_click(self, pos):
        x = pos[0]
        y = pos[1]
        if (x >= self.x1 and x <= self.x2) and (y >= self.y1 and y <= self.y2):
            return True
        return False
