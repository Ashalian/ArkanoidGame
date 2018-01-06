import pygame
from kolory import Colors

class Ball:
    def __init__(self, pos):
        self.colors = Colors(self)
        self.reset(pos)

    def moving(self):
        self.rect.x += self.leadXballChange
        self.rect.y += self.leadYballChange


    def reverseY(self):
        self.leadYballChange = -self.leadYballChange

    def reverseX(self):
        self.leadXballChange = -self.leadXballChange

    def tilt13(self):
        self.leadXballChange = self.leadXballChange*1.3

    def tilt07(self):
        self.leadXballChange = self.leadXballChange*0.7

    def reset(self, pos):
        self.rect = pygame.Rect(pos,680-10, 10, 10)
        self.leadXballChange = 7
        self.leadYballChange = -7
