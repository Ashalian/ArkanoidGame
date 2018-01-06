import pygame, sys
from kolory import Colors

class Tacka(object):

    def __init__(self, game):
        self.game = game
        self.leadX = 595
        self.leadY = 680
        self.rect = pygame.Rect(595, 680, 80, 10)
        self.colors = Colors(self)
    def draw(self):
        pygame.draw.rect(self.game.screen, self.colors.white, self.rect)

    def moving(self):

        if pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] and self.rect.left>10:
                self.rect.x -= 10

            if pressed[pygame.K_RIGHT] and self.rect.right +10 < 1280:
                self.rect.x += 10
