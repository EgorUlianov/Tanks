from random import randint
import os
import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 50

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Tank:
    image1 = load_image('t1 left.png')
    image2 = load_image('t2 left.png')
    def __init__(self, player, px, py, direct, keyList):

        objects.append(self)
        self.type = 'tank'

        self.player = player
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 2
        self.hp = 5

        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]
        if self.player == 1:
            self.image = Tank.image1
        elif self.player == 2:
            self.image = Tank.image2
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def update(self):
        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            if self.player == 1:
                self.image = Tank.image1
            elif self.player == 2:
                self.image = Tank.image2
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
            if self.player == 1:
                self.image = pygame.transform.flip(Tank.image1, True, False)
            elif self.player == 2:
                self.image = pygame.transform.flip(Tank.image2, True, False)
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            if self.player == 1:
                self.image = pygame.transform.rotate(Tank.image1, -90)
            elif self.player == 2:
                self.image = pygame.transform.rotate(Tank.image2, -90)
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
            if self.player == 1:
                self.image = pygame.transform.rotate(Tank.image1, 90)
            elif self.player == 2:
                self.image = pygame.transform.rotate(Tank.image2, 90)

        for obj in objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')


class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(window, 'green', self.rect)
        pygame.draw.rect(window, 'gray20', self.rect, 2)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)


bullets = []
objects = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))

for _ in range(50):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(0, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True

        if not fined:
            break

    Block(x, y, TILE)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    for bullet in bullets:
        bullet.update()


    window.fill('black')
    for bullet in bullets:
        bullet.draw()


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()