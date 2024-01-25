import pygame
import scripts.tools as tools
from scripts.scenes.language_menu import LanguageScene
from scripts.scenes.control_menu import ControlScene

from data.language import russian, english


pygame.init()

font = pygame.font.SysFont('Impact', 85)


class Menu:
    def __init__(self):
        self.option_surflaces: list[str] = list()
        self.option_callback = list()
        self.current_option_index = 0
        self.is_action_menu = True

    def append_option(self, option: str, callback) -> None:
        self.option_surflaces.append(option)
        self.option_callback.append(callback)

    def switch(self, direction: int) -> None:
        if self.is_action_menu:
            self.current_option_index = (self.current_option_index + direction) % len(self.option_callback)

    def select(self):
        if self.is_action_menu:
            return self.option_callback[self.current_option_index]()


    @staticmethod
    def hover(mos_pos: tuple[int, int], screen: pygame.Surface, virtual_surface: pygame.Surface) -> tuple[int, int]:
        x_coeff = virtual_surface.get_width() / screen.get_width()
        y_coeff = virtual_surface.get_height() / screen.get_height()
        return int(mos_pos[0] * x_coeff), int(mos_pos[1] * y_coeff)

    def draw(self, surface: pygame.Surface, option_y_padding: int, screen: pygame.Surface, settings: dict) -> None:
        x, y = surface.get_width() * 0.75, surface.get_height() * 0.6
        if settings['Language'] == 'English':
            lang = english.eng
        elif settings['Language'] == 'Русский':
            lang = russian.rus

        for i, option in enumerate(self.option_surflaces):  # проходимся по всем повехностям
            # создаём прямоугольник описывающий текст2
            option = font.render(lang[option], True, pygame.Color((255, 228, 225)))
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y_padding)
            if self.is_action_menu:
                if option_rect.collidepoint(self.hover(pygame.mouse.get_pos(), screen, surface)):
                    # проверяем на пересечение с мышкой
                    # и меняем текущий выбранный элемент на тот, на который указывает мышь
                    self.current_option_index = i
            if i == self.current_option_index:  # если текущий элемент выбранн, создаём подчёркивание для него
                underline = pygame.Surface((option.get_width(), 9))
                underline.fill(pygame.Color((255, 228, 225)))
                underline_pos = (option_rect.x, option_rect.bottom - option_y_padding // 5)
            surface.blit(option, option_rect)  # отрисовываем текст
        surface.blit(underline, underline_pos)  # отрисовываем подчёркивание

    def check_mouse_event(self, x, y, option_y_padding, screen, surf):
        # метод находящий элемент на который указывает мышь
        if self.is_action_menu:
            for i, option in enumerate(self.option_surflaces):
                option = font.render(option, True, pygame.Color((255, 255, 255)))
                option_rect = option.get_rect()
                option_rect.topleft = (x, y + i * option_y_padding)
                if option_rect.collidepoint(self.hover(pygame.mouse.get_pos(), screen, surf)):
                    return self.select()


def menu_scene(screen: pygame.Surface, virtual_surface: pygame.Surface, switch_scene, settings: dict) -> None:
    # меню игры
    extra_scene = None  # переменная хранящая текущую доп сцену (с выбором языка или настроек)
    menu = Menu()  # создание меню

    def open_play():
        global play
        play = True
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
                tanks.clear()
                clock.tick(1)
                objects.clear()
                clock.tick(1)
                bushes.clear()
                clock.tick(1)
                bullets.clear()
                clock.tick(1)
                level += 1
                if level < len(maps):
                    generate_level(load_level(maps[level]))
                else:
                    play = False


    def open_language_scene():  # функция открывающая окно выбора языка и блокирующая меню
        nonlocal extra_scene, menu, virtual_surface
        extra_scene = LanguageScene(*virtual_surface.get_size(), settings)  # создание меню выбора языков
        menu.is_action_menu = False  # блокировка меню

    def open_settings_scene():
        nonlocal extra_scene, menu, virtual_surface
        extra_scene = ControlScene(*virtual_surface.get_size(), settings)
        menu.is_action_menu = False

    # создание кнопок меню
    menu.append_option('Play', open_play)  # действий пока нет
    menu.append_option('Control', open_settings_scene)  # открывает окно изменения настроек
    menu.append_option('Language', open_language_scene)  # открывает окно выбора языка
    menu.append_option('Exit', lambda: 'Exit')  # выполняет выход из игры

    # загружаем задний фон
    background = tools.load_image('initial background.jpg')
    background = pygame.transform.scale(background, virtual_surface.get_size())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                switch_scene(None)
            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                # изменение выбранного элеметна меню с помощью стрелочек
                if key[pygame.K_UP]:
                    menu.switch(-1)
                elif key[pygame.K_DOWN]:
                    menu.switch(1)
                elif key[pygame.K_RETURN]:
                    if menu.select() == 'Exit':  # если функция вернула Exit - закрываем игру
                        running = False
                        switch_scene(None)
            if event.type == pygame.MOUSEBUTTONDOWN:  # обработка нажатий мыши
                if menu.check_mouse_event(50, 600, 70, screen, virtual_surface) == 'Exit':
                    running = False
                    switch_scene(None)
            if extra_scene is not None:
                if extra_scene.handle_event(event, virtual_surface, screen) == 'Close':
                    extra_scene = None
                    menu.is_action_menu = True
        # отрисовываем всё на сцене
        virtual_surface.fill((0, 0, 0))
        virtual_surface.blit(background, (0, 0))
        menu.draw(virtual_surface, 70, screen, settings)
        if extra_scene is not None:
            extra_scene.draw(virtual_surface)
        # отрисовываем сцену на экране
        scaled_surface = pygame.transform.scale(virtual_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
