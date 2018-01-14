import pygame, sys


class Ball:
    def __init__(self, pos):
        self.reset(pos)

    def moving(self):
        self.rect.x += self.leadXballChange
        self.rect.y += self.leadYballChange

    def reverseY(self):
        self.leadYballChange = -self.leadYballChange

    def reverseX(self):
        self.leadXballChange = -self.leadXballChange

    def tilt13(self):
        self.leadXballChange = self.leadXballChange * 1.3

    def tilt07(self):
        self.leadXballChange = self.leadXballChange * 0.7

    def reset(self, pos):
        self.rect = pygame.Rect(pos, 680 - 10, 10, 10)
        self.leadXballChange = 7
        self.leadYballChange = -7

    def BallMoveBeforeSpace(self):
        if pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] and self.rect.left > 50:
                self.rect.x -= 10

            if pressed[pygame.K_RIGHT] and self.rect.right + 50 < 1280:
                self.rect.x += 10


class Tacka(object):
    def __init__(self, game):
        self.game = game
        self.leadX = 595
        self.leadY = 680
        self.rect = pygame.Rect(595, 680, 80, 10)
        self.Colors = Colors

    def draw(self):
        pygame.draw.rect(self.game.screen, self.Colors.white, self.rect)

    def moving(self):

        if pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] and self.rect.left > 10:
                self.rect.x -= 10

            if pressed[pygame.K_RIGHT] and self.rect.right + 10 < 1280:
                self.rect.x += 10


class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (100, 200, 0)


class Block:
    def __init__(self, rect):
        self.rect = rect


class Game(object):
    def __init__(self):

        # Inicjalizacja
        self.widthScreen = 1280
        self.heightScreen = 720
        self.top = pygame.Rect(0, 0, self.widthScreen, 10)
        self.left = pygame.Rect(0, 0, 10, self.heightScreen)
        self.right = pygame.Rect(self.widthScreen - 10, 0, 10, self.heightScreen)

        pygame.init()
        pygame.display.set_caption('ArkanoidMateuszFicek')
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((self.widthScreen, self.heightScreen))

        self.player = Tacka(self)
        self.ball = Ball(632)
        self.colors = Colors()
        self.startOfGame()
        clock = pygame.time.Clock()
        self.spaceCount = 0
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
                    if pressed[pygame.K_SPACE]:
                        self.spaceCount = 1
            # Rysowanie
            clock.tick(60)
            self.screen.fill((40, 40, 90))
            if self.spaceCount == 1:
                self.BallMove()
            self.draw()
            self.tick()
            pygame.display.flip()

    def draw(self):
        self.player.draw()
        pygame.draw.rect(self.screen, self.colors.white, self.top)
        pygame.draw.rect(self.screen, self.colors.white, self.left)
        pygame.draw.rect(self.screen, self.colors.white, self.right)
        pygame.draw.rect(self.screen, (250, 130, 20), self.ball.rect)

        for self.block in self.blocks:
            pygame.draw.rect(self.screen, self.colors.green, self.block)
            # for blocks in self.blocksRed:
            #   pygame.draw.rect(self.screen, self.colors.red, blocks)

    def BallMove(self):
        self.ball.moving()

    def tick(self):

        self.player.moving()
        if self.spaceCount == 0:
            self.ball.BallMoveBeforeSpace()

        # COLLISION DETECTION
        # EDGES
        if self.spaceCount == 1:
            if self.ball.rect.left <= self.left.right:
                self.ball.reverseX()
            if self.ball.rect.right >= self.right.left:
                self.ball.reverseX()
            if self.ball.rect.top <= self.top.bottom:
                self.ball.reverseY()

            # PADDLE
            if self.ball.rect.bottom == self.player.rect.top and self.ball.rect.bottom <= self.heightScreen and self.ball.rect.centerx < self.player.rect.right and self.ball.rect.centerx + 5 > self.player.rect.left:
                self.ball.reverseY()
                if self.player.rect.right - self.ball.rect.centerx <= 20 and not self.ball.rect.right == self.left.right:
                    self.ball.reverseX()
                if self.player.rect.right - self.ball.rect.centerx >= 70:
                    self.ball.reverseX()

            # BLOCKS
            collisionIndex = self.ball.rect.collidelist(self.blocks)
            if collisionIndex != -1:
                self.ball.reverseY()
                self.blocks.pop(collisionIndex)
                if (len(self.blocks)) <= 0:
                    self.win()

        # FLYING DOWN
        if self.ball.rect.top >= self.heightScreen:
            self.ball.reset(self.player.rect.centerx)
            pygame.time.wait(2000)
            self.lives -= 1
            self.spaceCount = 0
            self.lose()

    def startOfGame(self):
        self.blocks = [pygame.Rect(50 + self.widthScreen / 9 * x, 32 + self.widthScreen / 12 * y, 64, 16) for x in
                       range(9) for y in range(3)]
        self.lives = 5

    def Level2(self):
        # self.blocksRed = [pygame.Rect(50 + self.widthScreen / 5 * x, 32 + self.widthScreen / 18 * y, 64, 16) for x in range(5) for y in range(3)]
        pass

    def win(self):
        exit(0)

    def lose(self):
        if self.lives == 0:
            exit(0)


if __name__ == "__main__":
    Game()
