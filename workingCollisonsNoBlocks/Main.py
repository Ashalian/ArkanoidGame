import pygame, sys, kolory
from Tacka import Tacka
from kulka import Ball
from kolory import Colors
class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
class Game(object):
    def __init__(self):

        # Inicjalizacja
        self.widthScreen = 1280
        self.heightScreen = 720
        self.top = pygame.Rect(0,0,self.widthScreen, 10)
        self.left = pygame.Rect(0,0,10,self.heightScreen)
        self.right = pygame.Rect(self.widthScreen-10,0,10,self.heightScreen)


        pygame.init()
        pygame.display.set_caption('ArkanoidMateuszFicek')
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((self.widthScreen, self.heightScreen))


        self.player = Tacka(self)
        self.ball = Ball(640)
        self.colors = Colors()

        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                #if event.type == pygame.KEYDOWN:
                 #   if event.key == pygame.K_SPACE:
                  #      self.ball.leadXballChange = 5
                   #     self.ball.leadYballChange = -5

                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_LEFT] and self.player.leadX > 0:
                        self.player.leadX -= 10
                    if pressed[pygame.K_RIGHT] and self.player.leadX + 80 < 1280:
                        self.player.leadX += 10
            # Rysowanie
            clock.tick(60)
            self.screen.fill((40,40,90))
            self.draw()
            self.tick()
            pygame.display.flip()

    def draw(self):
        self.ball.moving()
        self.player.draw()
        pygame.draw.rect(self.screen, self.colors.white, self.top)
        pygame.draw.rect(self.screen, self.colors.white, self.left)
        pygame.draw.rect(self.screen, self.colors.white, self.right)
        pygame.draw.rect(self.screen, (250,130,20), self.ball.rect)


    def tick(self):
        self.ball.moving()
        self.player.moving()

        #COLLISION DETECTION
        #EDGES
        if self.ball.rect.right-8 <= 10:
            self.ball.reverseX()
        if self.ball.rect.right >= 1270:
            self.ball.reverseX()
        if self.ball.rect.top <= self.top.bottom:
            self.ball.reverseY()

        #PADDLE
        if self.ball.rect.bottom == self.player.rect.top and self.ball.rect.bottom <= self.heightScreen and self.ball.rect.centerx-5 < self.player.rect.right and self.ball.rect.centerx+5 > self.player.rect.left:
            self.ball.reverseY()
        if self.ball.rect.left == self.player.rect.right and self.ball.rect.centery+5 < self.player.rect.right and self.ball.rect.centery+5 > self.player.rect.right:
            self.ball.reverseX()
if __name__ == "__main__":
    Game()
