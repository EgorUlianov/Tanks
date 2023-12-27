import os
import pygame
import sys

pygame.init()
size = 1000, 1000
screen = pygame.display.set_mode(size)
screen.fill((0, 255, 0))
clock = pygame.time.Clock()


# Загрузка картинок
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


# Класс танка
class Tank1(pygame.sprite.Sprite):
    image = load_image('tiger.png')

    # Загрузка картинки
    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(group)
        self.image = Tank1.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    # Обработка нажатий на стрелочки
    def update(self, event):
        if event[pygame.K_UP]:
            self.rect = self.rect.move(0, -10)
            self.image = pygame.transform.rotate(Tank1.image, -90)
        if event[pygame.K_DOWN]:
            self.rect = self.rect.move(0, 10)
            self.image = pygame.transform.rotate(Tank1.image, 90)
        if event[pygame.K_RIGHT]:
            self.rect = self.rect.move(10, 0)
            self.image = pygame.transform.flip(Tank1.image, True, False)
        if event[pygame.K_LEFT]:
            self.rect = self.rect.move(-10, 0)
            self.image = Tank1.image


class Tank2(pygame.sprite.Sprite):
    image = load_image('tiger.png')

    # Загрузка картинки
    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(group)
        self.image = Tank2.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    # Обработка нажатий на стрелочки
    def update(self, event):
        if event[pygame.K_w]:
            self.rect = self.rect.move(0, -10)
            self.image = pygame.transform.rotate(Tank2.image, -90)
        if event[pygame.K_s]:
            self.rect = self.rect.move(0, 10)
            self.image = pygame.transform.rotate(Tank2.image, 90)
        if event[pygame.K_d]:
            self.rect = self.rect.move(10, 0)
            self.image = pygame.transform.flip(Tank2.image, True, False)
        if event[pygame.K_a]:
            self.rect = self.rect.move(-10, 0)
            self.image = Tank2.image


# Запуск
def main():
    all_sprites = pygame.sprite.Group()
    Tank1(all_sprites)
    Tank2(all_sprites)
    running = True
    while running:
        keys = pygame.key.get_pressed()
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False
        all_sprites.update(keys)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(40)
    pygame.quit()


if __name__ == '__main__':
    main()