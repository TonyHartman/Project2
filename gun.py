import math
from random import choice
from random import randint
import pygame


def distanсe(x1, y1, x2, y2, x3, y3):
    """Считает расстояние между точками прямой, построенной по точкам (x1, y1) и (x2, y2), и точкой (x3, y3)"""
    d = math.fabs((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    return d


FPS = 30

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HIGHT = 600
death_time = 200
score = 0
g = 5


class Ball:
    def __init__(self, screen: pygame.Surface, x=20, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение центра мяча по горизонтали
        y - начальное положение центра мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
            и стен по краям окна (размер окна WIDTHхHIGHT), "потолка" нет. Также мяч отскакивает от пола с затуханием.
        """
        if self.vx >= 0 and (self.x + self.r + self.vx) >= WIDTH:
            self.x = WIDTH - self.vx + (WIDTH - self.x - self.r)
            self.vx = -self.vx
        if self.vx <= 0 and (self.x - self.r + self.vx) <= 0:
            self.x = -self.vx + self.r - self.x
            self.vx = -self.vx
        if self.vy >= 0 and (self.y + self.r + self.vy) >= HIGHT:
            self.vy = -0.7 * self.vy
        else:
            self.x += self.vx
            self.y += self.vy
            self.vy += g

    def draw(self):
        if self.live <= death_time:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
                )
            self.live += 1

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """

        d = distanсe(self.x, self.y, self.x + self.vx, self.y + self.vy, obj.x, obj.y)
        if d < (self.r + obj.r) and\
                ((self.x - obj.x) * (self.x + self.vx - obj.x) <= 0 or
                 (self.y - obj.y) * (self.y + self.vy - obj.y) <= 0):
            return True
        else:
            return False
        '''
        if math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2) <= self.r + obj.r:
            return True
        else:
            return False
        '''


class Bang:
    def __init__(self, screen: pygame.Surface, x=20, y=450):
        self.screen = screen
        self.color = WHITE
        self.x = x
        self.y = y
        self.r = 0
        self.v = 10

    def new_bang(self):
        global bangs
        bang = Bang(self.screen, gun.x, gun.y)
        bangs.append(bang)

    def move(self):
        self.r += self.v

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r, 4)


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 30
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.x = self.x + self.f2_power * math.cos(self.an)
        new_ball.y = self.y + self.f2_power * math.sin(self.an)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def motion_right(self):
        self.x += 10

    def motion_left(self):
        self.x -= 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0] - self.x) == 0 and event.pos[1] <= self.y:
                self.an = math.pi / 2
            elif (event.pos[0] - self.x) == 0 and event.pos[1] >= self.y:
                self.an = -math.pi / 2
            elif event.pos[0] <= self.x:
                self.an = math.pi + math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
            elif event.pos[0] >= self.x:
                self.an = math.atan((event.pos[1] - self.y) / (event.pos[0] - self.x))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Рисует пушку"""
        pygame.draw.rect(self.screen, self.color, (self.x - 50, self.y + 20, 100, 40))
        pygame.draw.circle(self.screen, self.color, (self.x, self.y + 20), 21)
        pygame.draw.line(self.screen, self.color,
                         [self.x, self.y],
                         [self.x + self.f2_power * math.cos(self.an), self.y + self.f2_power * math.sin(self.an)], 5)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = WHITE
        else:
            self.color = GREY


class Target:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса Target

        Args:
        x - положение центра мишени по горизонтали
        y - положение центра мишени по вертикали
        """
        self.screen = screen
        self.x = randint(100, 780)
        self.y = randint(0, 550)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.r = randint(10, 50)
        self.color = RED
        self.live = 1
        self.points = 1

    def new_target(self):
        """ Инициализация новой цели. """
        global targets
        new_tar = Target(self.screen)
        targets.append(new_tar)

    def hit(self, score):
        """Попадание шарика в цель."""
        score += self.points
        print(score)
        return(score)

    def hit_by_bang(self, obj):
        if math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2) <= self.r + obj.r and obj.r <= math.sqrt(WIDTH**2 + HIGHT**2):
            return True
        else:
            return False

    def move(self):
        """Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy,
        и обеспечивает отскок от краёв окна.
        """
        if self.vx >= 0 and (self.x + self.r + self.vx) >= WIDTH:
            self.vx = -self.vx
        if self.vx <= 0 and (self.x - self.r + self.vx) <= 0:
            self.vx = -self.vx
        if self.vy >= 0 and (self.y + self.r + self.vy) >= HIGHT:
            self.vy = -self.vy
        if self.vy <= 0 and (self.y - self.r + self.vy) <= 0:
            self.vy = -self.vy
        else:
            self.x += self.vx
            self.y += self.vy

    def draw(self):
            pygame.draw.circle(screen, RED, (self.x, self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HIGHT))
bullet = 0
balls = []
targets = []
bangs = []

t0 = 0
clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
bang = Bang(screen)
finished = False
while not finished:
    screen.fill(BLACK)
    gun.draw()
    for b in bangs:
        b.draw()
    for t in targets:
        if t.live == 1:
            t.draw()
        print(t.x, t.y, t.r)
    print()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            gun.motion_left()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            gun.motion_right()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            bang.new_bang()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    if t0 >= 5:
        t0 = 0
        target.new_target()
    else:
        t0 += 1
    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t) and t.live:
                t.live = 0
                score = target.hit(score)
    for b in bangs:
        b.move()
        for t in targets:
            if t.hit_by_bang(b) and t.live:
                t.live = 0
                score = target.hit(score)
    for t in targets:
        t.move()
    gun.power_up()
pygame.quit()

'''
Реализоваль несколько типов целей с различным характером движения.
Сделать пушку двигающимся танком.
Создать "бомбочки", которые будут сбрасывать цели на пушку.
Сделать несколько пушек, которые могут стрелять друг в друга.
'''


