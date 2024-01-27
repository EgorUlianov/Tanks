# загружаем нужные библиотеки и модули
import pygame
from scripts.scenes.menu import menu_scene
import scripts.tools as tools

# проводим инициализацию pygame
pygame.init()


default_options = tools.load_default_options()
settings = tools.load_user_options()
# Теперь user_options содержит значения из options.txt, и отсутствующие настройки добавлены из default_options
# Сохранение обновленных настроек в файл options.txt
tools.save_user_options(settings)

# создаём экран
info = pygame.display.Info()

# получение ширины и высоты монитора
screen_width = pygame.display.Info().current_w
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((800, 500), pygame.RESIZABLE)

# экран на котором всё будет рисоватся, а потом оно растянется
virtual_surface = pygame.Surface((screen_width, screen_height))

# переменная в которой будет храниться текущая сцена
current_scene = None


def switch_scene(scene):
    global current_scene
    current_scene = scene


switch_scene(menu_scene)
while current_scene is not None and current_scene != 'Game':
    current_scene(screen, virtual_surface, switch_scene, settings)


WIDTH, HEIGHT = 570, 627
FPS = 30
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
    pygame.image.load('data/metall wall.png'),
    pygame.image.load('data/floor.png'),
    pygame.image.load('data/bush.png')
]
# Танки
imgTanks = [
    [pygame.image.load('data/t1fr1.png'),
     pygame.image.load('data/t1fr2.png'),
     pygame.image.load('data/t1fr3.png'),
     pygame.image.load('data/t1fr4.png'),
     pygame.image.load('data/t1fr5.png'),
     pygame.image.load('data/t1fr6.png'),
     pygame.image.load('data/t1fr7.png')
     ],
    [pygame.image.load('data/t2fr1.png'),
     pygame.image.load('data/t2fr2.png'),
     pygame.image.load('data/t2fr3.png'),
     pygame.image.load('data/t2fr4.png'),
     pygame.image.load('data/t2fr5.png'),
     pygame.image.load('data/t2fr6.png'),
     pygame.image.load('data/t2fr7.png')
     ]
]
imgBangs = [
    pygame.image.load('data/bang1.png'),
    pygame.image.load('data/bang2.png'),
    pygame.image.load('data/bang3.png'),
]

maps = [
    'data/map1.txt',
    'data/map2.txt',
    'data/map3.txt'
]


DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Floor(x * TILE, (y + 1) * TILE, TILE)
            elif level[y][x] == '*':
                Block(x * TILE, (y + 1) * TILE, TILE)
            elif level[y][x] == '+':
                MetalBlock(x * TILE, (y + 1) * TILE, TILE)
            elif level[y][x] == '-':
                Bush(x * TILE, (y + 1) * TILE, TILE)
            elif level[y][x] == '@':
                Tank('Green', x * TILE, (y + 1) * TILE, 0,
                     (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))
            elif level[y][x] == '_':
                Tank('Blue', x * TILE, (y + 1) * TILE, -2, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))

# Прорисовка
class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for tank in tanks:
            if tank.type == 'tank':
                pygame.draw.rect(window, tank.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(tank.hp), 1, tank.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1


# Танк
class Tank:
    def __init__(self, color, px, py, direct, keyList):
        tanks.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.moveSpeed = 4
        self.hp = 5
        self.anim = 0
        self.shotTimer = 0
        self.shotDelay = 60
        self.bulletSpeed = 10
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
        self.image = pygame.transform.rotate(imgTanks[self.rank][self.anim], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    # Движение Танка
    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank][self.anim], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
            if self.anim == 6:
                self.anim = 0
            else:
                self.anim += 1
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
            if self.anim == 6:
                self.anim = 0
            else:
                self.anim += 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
            if self.anim == 6:
                self.anim = 0
            else:
                self.anim += 1
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2
            if self.anim == 6:
                self.anim = 0
            else:
                self.anim += 1
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
            tanks.remove(self)
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
                if obj != self.parent and obj.type != 'bang' and \
                        obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py, 0)
                    break
            for tank in tanks:
                if tank != self.parent and tank.rect.collidepoint(self.px, self.py):
                    tank.damage(self.damage)
                    bullets.remove(self)
                    Bang(self.px, self.py, 0)
                    break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 5)


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

    def damage(self, value):
        pass


class Floor:
    def __init__(self, px, py, size):
        objects.append(self)
        self.type = 'bang'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = -1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick[5], self.rect)

    def damage(self, value):
        pass


class Bush:
    def __init__(self, px, py, size):
        bushes.append(self)
        self.type = 'bang'

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = -1

    def update(self):
        pass

    def draw(self):
        window.blit(imgBrick[6], self.rect)

    def damage(self, value):
        pass


bullets = []
objects = []
tanks = []
bushes = []
ui = UI()
Border(0, 57, 0, HEIGHT)
Border(WIDTH, 0, WIDTH, HEIGHT)
Border(0, 57, WIDTH, 0)
Border(0, HEIGHT, WIDTH, HEIGHT)
# Рандом генерация
if current_scene == 'Game':
    play = True
else:
    play = False
level = 0
generate_level(load_level(maps[level]))

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    keys = pygame.key.get_pressed()

    for obj in objects: obj.update()
    for tank in tanks: tank.update()
    for bullet in bullets: bullet.update()
    for bush in bushes: bush.update()
    ui.update()

    window.fill('black')

    for obj in objects: obj.draw()
    for bullet in bullets: bullet.draw()
    for tank in tanks: tank.draw()
    for bush in bushes: bush.draw()
    ui.draw()
    pygame.display.update()
    clock.tick(FPS)
    if len(tanks) < 2:
        bullets.clear()

        window.fill('black')
        for obj in objects: obj.draw()
        for tank in tanks: tank.draw()
        for bush in bushes: bush.draw()
        pygame.display.update()
        clock.tick(1)
        objects.clear()
        window.fill('black')
        for tank in tanks: tank.draw()
        for bush in bushes: bush.draw()
        pygame.display.update()
        clock.tick(1)
        bushes.clear()
        window.fill('black')
        clock.tick(1)
        window.fill('black')
        for tank in tanks: tank.draw()
        pygame.display.update()
        tanks.clear()
        clock.tick(1)
        window.fill('black')
        pygame.display.update()
        clock.tick(1)
        if level != 2:
            level += 1

        generate_level(load_level(maps[level]))
pygame.quit()
