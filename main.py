import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
TILE = 57

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)
# Кирпичи и степени деградации
imgBrick = [
    pygame.image.load('data/brick1.png'),
    pygame.image.load('data/brick2.png'),
    pygame.image.load('data/brick3.png'),
    pygame.image.load('data/brick4.png'),
    pygame.image.load('data/metall wall.png')
]
# Танки
imgTanks = [
    pygame.image.load('data/t1.png'),
    pygame.image.load('data/t2.png')
]
imgBangs = [
    pygame.image.load('data/bang1.png'),
    pygame.image.load('data/bang2.png'),
    pygame.image.load('data/bang3.png'),
]

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


# Прорисовка
class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1


# Танк
class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
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
        if self.color == 'Blue':
            self.rank = 1
        elif self.color == 'Green':
            self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    # Движение Танка
    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for obj in objects:
            if obj != self and (obj.type == 'block' or obj.type == 'border') and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        # Стрельба
        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0: self.shotTimer -= 1

    def draw(self):
        window.blit(self.image, self.rect)

    # Получение урона
    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            Bang(self.rect.x, self.rect.y, 3)
            print(self.color, 'dead')


# Пули
class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage
    # Движение пули
    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py, 0)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


# Взрыв
class Bang:
    def __init__(self, px, py, frame):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = frame

    def update(self):
        self.frame += 0.2
        if self.frame >= 3: objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)


# Кирпичные стены
class Block:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 4

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick[self.hp - 1], self.rect)

    # Получение урона
    def damage(self, value):
        self.hp -= value
        if self.hp <= 0: objects.remove(self)


# Металлическая стенка
class MetalBlock:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'block'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = -1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick[4], self.rect)

    def damage(self, value):
        pass


# Границы, чтобы танки не уезжали за экран
class Border():
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        objects.append(self)
        self.type = 'border'
        if x1 == x2:  # вертикальная стенка
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)

    def update(self):
        pass

    def draw(self):
        pass


bullets = []
objects = []
Tank('Blue', 100, 275, -1, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tank('Green', 650, 275, -2, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))
ui = UI()
Border(0, 0, 0, HEIGHT)
Border(WIDTH, 0, WIDTH, HEIGHT)
Border(0, 0, WIDTH, 0)
Border(0, HEIGHT, WIDTH, HEIGHT)
# Рандом генерация
for _ in range(50):
    while True:
        x = randint(0, WIDTH // TILE - 1) * TILE
        y = randint(1, HEIGHT // TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect): fined = True

        if not fined: break

    Block(x, y, TILE)

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    for bullet in bullets: bullet.update()
    for obj in objects: obj.update()
    ui.update()

    window.fill('black')
    for bullet in bullets: bullet.draw()
    for obj in objects: obj.draw()
    ui.draw()
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()