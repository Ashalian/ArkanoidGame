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

    def reset(self, pos):

        self.rect = pygame.Rect(pos, 680 - 10, 10, 10)
        self.leadXballChange = 7
        self.leadYballChange = -7

    def BallMoveBeforeSpace(self):
        if pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT] and self.rect.left > 45:
                self.rect.x -= 10
                print(self.rect.x)
            if pressed[pygame.K_RIGHT] and self.rect.centerx < 1235:
                self.rect.x += 10


class Tacka(object):
    def __init__(self, game):
        self.game = game
        self.leadX = 595
        self.leadY = 680
        self.rect = pygame.Rect(595, 680, 80, 10)
        self.Colors = Colors

    def draw(self):
        pygame.draw.rect(self.game.screen, self.Colors.red, self.rect)

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
    red = (225, 67, 58)
    green = (100, 200, 0)
    orange = (240, 164, 52)
    darkOrange = (242, 91, 38)
    darkBlue = (64, 55, 98)
    offWhite = (211, 206, 202)


class Game(object):
    def __init__(self):

        # Inicjalizacja
        self.widthScreen = 1280
        self.heightScreen = 720
        self.top = pygame.Rect(0, 0, self.widthScreen, 10)
        self.left = pygame.Rect(0, 0, 10, self.heightScreen)
        self.right = pygame.Rect(self.widthScreen - 10, 0, 10, self.heightScreen)

        pygame.init()
        self.font = pygame.font.Font('SpaceMono-Regular.ttf', 18)
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
            self.screen.fill(self.colors.darkBlue)
            if self.spaceCount == 1:
                self.BallMove()
            self.draw()
            self.tick()
            self.lose()
            self.printMsg("Your score: %i" % self.points, self.colors.offWhite, [20, 690])
            self.printMsg("Your lives: %i" % self.lives, self.colors.offWhite, [1120, 690])

            pygame.display.flip()

    def draw(self):
        if self.points < 270:
            self.Level1()
        elif self.points >= 270 and self.points < 820:
            self.Level2()
        elif self.points >= 820 and self.points < 1700:
            self.Level3()
        elif self.points >= 1700:
            self.Level4()
        self.player.draw()
        pygame.draw.rect(self.screen, self.colors.white, self.top)
        pygame.draw.rect(self.screen, self.colors.white, self.left)
        pygame.draw.rect(self.screen, self.colors.white, self.right)
        pygame.draw.rect(self.screen, self.colors.offWhite, self.ball.rect)


    def BallMove(self):
        self.ball.moving()

    def printMsg(self, msg, color, pos):
        screenText = self.font.render(msg, True, color)
        self.screen.blit(screenText, pos)

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
            if self.ball.rect.top+5 <= self.top.bottom:
                self.ball.reverseY()

        # PADDLE
            if self.ball.rect.bottom == self.player.rect.top and self.ball.rect.bottom <= self.heightScreen and self.ball.rect.centerx < self.player.rect.right and self.ball.rect.centerx + 5 > self.player.rect.left:
                self.ball.reverseY()
                if self.player.rect.right - self.ball.rect.centerx <= 20 and not self.ball.rect.right == self.left.right and self.player.rect.right < 1200:
                    self.ball.reverseX()
                if self.player.rect.right - self.ball.rect.centerx >= 70 and self.player.rect.left > 80:
                    self.ball.reverseX()

        # BLOCKS HANDLED IN LEVELS

        # FLYING DOWN
        if self.ball.rect.top >= self.heightScreen:
            self.ball.reset(self.player.rect.centerx)
            pygame.time.wait(2000)
            self.lives -= 1
            self.spaceCount = 0
            self.lose()

    def startOfGame(self):
        self.points = 0

        self.blocks = [pygame.Rect(40 + self.widthScreen / 9 * x, 32 + self.widthScreen / 12 * y, 64, 16) for x in
                       range(9) for y in range(3)]
        self.blocksRed = [pygame.Rect(83 + self.widthScreen / 12 * x, 32 + self.widthScreen / 18 * y, 48, 16) for x in
                          range(11) for y in range(5)]

        self.blocksBlue = [pygame.Rect(53 + self.widthScreen / 12 * x, 32 + self.heightScreen / 18 * y, 80, 10) for x in
                           range(11) for y in range(8)]

        self.blocksGreen = [pygame.Rect(16 + self.widthScreen / 24 * x, 32 + self.heightScreen / 18 * y, 20, 10) for x
                            in range(24) for y in range(10)]

        self.lives = 5

    def Level1(self):
        for self.block in self.blocks:
            pygame.draw.rect(self.screen, self.colors.orange, self.block)
        collisionIndex = self.ball.rect.collidelist(self.blocks)
        if collisionIndex != -1:
            self.ball.reverseY()
            self.blocks.pop(collisionIndex)
            self.points += 10

    def Level2(self):
        self.screen.fill(self.colors.offWhite)
        for self.block in self.blocksRed:
            pygame.draw.rect(self.screen, self.colors.darkOrange, self.block)
        collisionIndexRed = self.ball.rect.collidelist(self.blocksRed)
        if collisionIndexRed != -1:
            self.ball.reverseY()
            self.blocksRed.pop(collisionIndexRed)
            self.points += 10

    def Level3(self):
        self.screen.fill(self.colors.darkOrange)
        for self.block in self.blocksBlue:
            pygame.draw.rect(self.screen, self.colors.offWhite, self.block)
        collisionIndexBlue = self.ball.rect.collidelist(self.blocksBlue)
        if collisionIndexBlue != -1:
            self.ball.reverseY()
            self.blocksBlue.pop(collisionIndexBlue)
            self.points += 10

    def Level4(self):
        self.screen.fill(self.colors.black)
        for self.block in self.blocksGreen:
            pygame.draw.rect(self.screen, self.colors.offWhite, self.block)
        collisionIndexGreen = self.ball.rect.collidelist(self.blocksGreen)
        if collisionIndexGreen != -1:
            self.ball.reverseY()
            self.blocksGreen.pop(collisionIndexGreen)
            self.points += 10

    def win(self):
        self.screen.fill(self.colors.black)
        self.font = pygame.font.Font('SpaceMono-Regular.ttf', 48)
        screenText = self.font.render("You won! Your score: %i" % self.points, True, self.colors.offWhite)
        self.screen.blit(screenText, [250, 300])
        pygame.display.flip()
        pygame.time.wait(4000)
        exit(0)

    def lose(self):
        if self.lives == 0:
            self.screen.fill(self.colors.black)
            self.font = pygame.font.Font('SpaceMono-Regular.ttf', 48)
            screenText = self.font.render("You lost! Your score: %i" % self.points, True, self.colors.offWhite)
            self.screen.blit(screenText, [250,300])
            pygame.display.flip()
            pygame.time.wait(4000)
            exit(0)


if __name__ == "__main__":
    Game()
