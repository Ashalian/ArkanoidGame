import pygame, sys, kolory
from Tacka import Tacka
from kulka import Ball
from kolory import Colors
from os import path
class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (200,200,0)
class Block:
    def __init__(self, rect):
        self.rect = rect

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
        self.startOfGame()
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_LEFT] and self.player.leadX > 0:
                        self.player.leadX -= 5
                    if pressed[pygame.K_RIGHT] and self.player.leadX + 80 < 1280:
                        self.player.leadX += 5
            # Rysowanie
            clock.tick(60)
            self.screen.fill((40,40,90))
            self.draw()
            self.tick()
            pygame.display.flip()

    def draw(self):
        self.player.draw()
        pygame.draw.rect(self.screen, self.colors.white, self.top)
        pygame.draw.rect(self.screen, self.colors.white, self.left)
        pygame.draw.rect(self.screen, self.colors.white, self.right)
        pygame.draw.rect(self.screen, (250,130,20), self.ball.rect)

        for block in self.blocks:
            pygame.draw.rect(self.screen, self.colors.green, block)

        #for blocks in self.blocksRed:
         #   pygame.draw.rect(self.screen, self.colors.red, blocks)




    def tick(self):
        self.ball.moving()
        self.player.moving()

        #COLLISION DETECTION
        #EDGES
        if self.ball.rect.left <= self.left.right:
            self.ball.reverseX()
        if self.ball.rect.right >= self.right.left:
            self.ball.reverseX()
        if self.ball.rect.top <= self.top.bottom:
            self.ball.reverseY()
        print(self.ball.rect.right)
        print(self.left.right)

        #PADDLE
        if self.ball.rect.bottom == self.player.rect.top and self.ball.rect.bottom <= self.heightScreen and self.ball.rect.centerx < self.player.rect.right and self.ball.rect.centerx+5 > self.player.rect.left:
            self.ball.reverseY()
            if self.player.rect.right - self.ball.rect.centerx <= 20 and not self.ball.rect.right == self.left.right:
                self.ball.reverseX()
            if self.player.rect.right - self.ball.rect.centerx >= 70:
                self.ball.reverseX()


        #BLOCKS
        collisionIndex = self.ball.rect.collidelist(self.blocks)
        if collisionIndex != -1:
            self.ball.reverseY()
            self.blocks.pop(collisionIndex)

            if (len(self.blocks))<=0:
                self.win()

        #FLYING DOWN
        if self.ball.rect.top >= self.heightScreen:
            self.ball.reset(self.player.rect.centerx)
            pygame.time.wait(2000)
            self.lives-=1
            self.lose()



    def startOfGame(self):
        self.blocks = [pygame.Rect(50 + self.widthScreen / 9 * x, 32 + self.widthScreen / 12 * y, 64, 16) for x in range(9) for y in range(3)]
        self.lives = 5
    def Level2(self):
        #self.blocksRed = [pygame.Rect(50 + self.widthScreen / 5 * x, 32 + self.widthScreen / 18 * y, 64, 16) for x in range(5) for y in range(3)]
        pass
    def win(self):
        exit(0)

    def lose(self):
        if self.lives==0:
            exit(0)

if __name__ == "__main__":
    Game()
