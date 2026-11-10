import sys, random
import pygame as pg
import pygame.freetype


# Определяем некоторые цвета
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
GREEN = (30, 122, 13)
RED = (217, 17, 17)
LEMON = (229, 240, 31)
ORANGE = (247, 117, 25)

W, H = (1000, 600)

pg.mixer.init()

# классы, функции

class Puddle:
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)
        self.speed = 6

    def move(self, dy):
        self.rect.y += dy
        if self.rect.y <= 15:
            self.rect.y = 15
        if self.rect.bottom >= H - 15:
            self.rect.bottom = H - 15


    def draw(self, screen, color):
        pg.draw.rect(screen, color, self.rect)

# class Player(Puddle):
#     ...

class Computer(Puddle):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.speed = 8
    def update(self, ball):
        if ball.rect.centerx > W // 2 and ball.dx > 0:
            if self.rect.bottom < ball.rect.top:
                self.move(self.speed)
            elif self.rect.top > ball.rect.bottom:
                self.move(-self.speed)


class Ball:
    def __init__(self, x, y):
        self.rect = pg.Rect(x, y, 25, 25)
        self.startspeed = 6
        self.speed = 6
        self.getrandom_direction()
        self.pingpongsound = pg.mixer.Sound("pingpongsound.wav")

    def getrandom_direction(self):
        self.dx = random.choice([self.speed, -self.speed])
        self.dy = random.choice([self.speed, -self.speed])

    def update(self, player, opponent):
        self.rect.x += self.dx
        self.rect.y -= self.dy
        if self.rect.y <= 0 or self.rect.bottom >= H:
            self.dy = -self.dy
        self.prove_collide(player, "left")
        self.prove_collide(opponent, "right")

    def draw(self, screen, color):
        pg.draw.ellipse(screen, color, self.rect)

    def prove_collide(self, currentpuddle, side):
        if side == "left":
            if self.rect.colliderect(currentpuddle) and self.dx < 0:
                self.dx = -self.dx
                self.pingpongsound.play()
                self.speed += 0
                print(self.speed)
        elif side == "right":
            if self.rect.colliderect(currentpuddle) and self.dx > 0:
                self.dx = -self.dx
                self.pingpongsound.play()
                self.speed += 0
                print(self.speed)

    def restart_ball(self):
        self.getrandom_direction()
        self.rect.center = W // 2, H // 2
        self.speed = self.startspeed




class Game:
    def __init__(self):
        pg.init()
        self.size = (W, H)
        self.okno = pg.display.set_mode(self.size)
        self.finishgamewin = False
        self.targetscore = 10
        pg.display.set_caption("Ping Pong")

        self.clock = pg.time.Clock()
        self.fps = 60
        self.player = Puddle(20, self.size[1] // 2 - (105 // 2), 12, 105)
        self.playerspeed = 0
        self.playerscore = 0
        self.ball = Ball(self.size[0] // 2 - 11, self.size[1] // 2 - 11)
        self.opponent = Computer(970, self.size[1] // 2 - (105 // 2), 12, 105)
        self.opponentscore = 0
        self.font1 = pg.freetype.Font("CascadiaMono.ttf", 42)
        self.resulttext = ''
        self.restarttext = ''

    def restartgame(self):
        self.finishgamewin = False
        self.restarttext = ''
        self.resulttext = ''
        pg.draw.line(self.okno, WHITE, (self.size[0] // 2, self.size[1]), (self.size[0] // 2, 0))
        self.playerscore = 0
        self.opponentscore = 0


    def run_game(self):
        lemon = True
        while lemon:
            for event in pg.event.get():    # Обрабатываем события
                if event.type == pg.QUIT:
                    lemon = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        self.playerspeed = -self.player.speed
                    if event.key == pg.K_s:
                        self.playerspeed = self.player.speed
                    if event.key == pg.K_r and self.finishgamewin:
                       self.restartgame()
                if event.type == pg.KEYUP:
                    self.playerspeed = 0

            # Логика игры должна находиться здесь
            if not self.finishgamewin:
                self.player.move(self.playerspeed)
                self.opponent.update(self.ball)
                self.ball.update(self.player, self.opponent)
            if self.ball.rect.right <= 0:
                self.ball.restart_ball()
                self.opponentscore += 1
                print(self.opponentscore)
                if self.opponentscore >= self.targetscore:
                    self.finishgamewin = True
                    self.resulttext = "  AI won"
                    self.restarttext = "Click R to restart"
            if self.ball.rect.left >= self.size[0]:
                self.ball.restart_ball()
                self.playerscore += 1
                print(self.playerscore)
                if self.playerscore >= self.targetscore:
                    self.finishgamewin = True
                    self.resulttext = "  You won"
                    self.restarttext = "Click R to restart"

            # Рисование объектов на экране должно происходить здесь

            self.okno.fill(GREEN)
            self.player.draw(self.okno, BLACK)
            self.opponent.draw(self.okno, RED)
            self.ball.draw(self.okno, ORANGE)
            self.font1.render_to(self.okno, (self.size[0] // 4, 20), str(self.playerscore), fgcolor=WHITE)
            self.font1.render_to(self.okno, (self.size[0] - (self.size[0] // 4), 20), str(self.opponentscore), fgcolor=WHITE)
            if not self.finishgamewin:
                pg.draw.line(self.okno, WHITE, (self.size[0] // 2, self.size[1]), (self.size[0] // 2, 0))
            if self.finishgamewin:
                self.font1.render_to(self.okno, (self.size[0] // 2 - 125, 20), self.resulttext, fgcolor=BLACK)
                self.font1.render_to(self.okno, (self.size[0] // 2 - 215, 60), self.restarttext, fgcolor=BLACK)

            pg.display.flip()
            self.clock.tick(self.fps)

        pg.quit()
game = Game()
game.run_game()