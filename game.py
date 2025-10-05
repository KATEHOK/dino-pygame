import pygame
from random import randint, random
from utils import load_img
from dino import Dino
from bg import  Bg
from bird import Bird

class Game:
    __is_running: bool
    __fps: float
    __screen_size: tuple[float, float]
    __plane_y: float
    __dino: Dino
    __bg: Bg
    __birds: set[Bird]
    __frame_id: int
    __base_speed: float
    __speed_multiplier: float

    def __init__(
            self,
            fps: float = 90,
            screen_size: tuple[float, float] = (1200, 600),
            speed: float = 100,
    ):
        self.__is_running = False
        self.__fps = fps
        self.__screen_size = screen_size
        self.__base_speed = speed
        self.__speed_multiplier = 1

        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__init_screen()

        self.__plane_y = self.__screen_size[1] * 0.75
        self.__birds = set()
        self.__dino = Dino(
            fps=self.__fps,
            x=self.__screen_size[0] * 0.2, y=self.__plane_y,
            jump_height=self.__screen_size[1] * 0.4, jump_duration=0.75,
            animation_duration=0.1
        )

        self.__bg = Bg(self.__screen_size, self.__fps, self.__speed)


    def start(self):
        """Запуск игры"""
        self.__frame_id = 0
        self.__is_running = True
        self.__loop()


    def __loop(self):
        """Игровой цикл"""
        while self.__is_running:
            self.__tick_rate()

            self.__before_render()
            self.__render()
            self.__after_render()

            self.__handle_key_press()
            self.__handle_events()

            self.__frame_id += 1


    def __before_render(self):
        """Действия с объектами до отрисовки"""
        self.__bg.before_render()
        self.__add_creatures()
        for bird in self.__birds:
            bird.before_render()
        self.__dino.before_render()


    def __render(self):
        """Отрисовка объектов"""
        self.screen.fill((255, 255, 255))
        self.__bg.blit(self.screen)
        for bird in self.__birds:
            bird.blit(self.screen)
        self.__dino.blit(self.screen)
        pygame.display.update()


    def __after_render(self):
        """Действия с объектами после отрисовки"""
        for bird in self.__birds.copy():
            self.__birds.remove(bird) if bird.is_outsider else bird.after_render()
        self.__dino.after_render()


    def __handle_key_press(self):
        """Обработка нажатий клавиш"""
        keys = pygame.key.get_pressed()
        # прыжок
        if keys[pygame.K_SPACE]:
            self.__dino.jump()


    def __handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit()
            # приседание
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                self.__dino.duck()
            elif event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
                self.__dino.unduck()


    def __add_creatures(self):
        """Добавляет существ (птиц и кактусы)"""
        if self.__frame_id % (self.__fps * randint(1, 3)) == 0:
            if len(self.__birds) < 2:
                self.__birds.add(Bird(
                    self.__fps,
                    self.__screen_size[0],
                    self.__plane_y - 2 * self.__dino.height * random(),
                    self.__bird_speed
                ))


    def __speedup(self, percent: float = 10):
        """Ускоряет набегающие объекты"""
        self.__speed_multiplier *= (1 + percent / 100)
        self.__bg.speedup(percent)


    def __quit(self):
        """Завершение игры"""
        self.__is_running = False
        pygame.quit()


    def __tick_rate(self):
        """Устанавливает fps для итерации цикла"""
        self.__clock.tick(self.__fps)


    def __init_screen(
            self,
            screen_size: tuple[float, float] = None,
            caption: str = "Dino",
            icon_directory: str = "./img",
            icon_filename: str = "icon",
            icon_extension: str = "png"
    ):
        """Инициализация игрового окна"""
        if screen_size is None:
            screen_size = self.__screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)
        pygame.display.set_icon(load_img(icon_directory, icon_filename, icon_extension))


    @property
    def __speed(self) -> float:
        return self.__base_speed * self.__speed_multiplier

    @property
    def __bird_speed(self):
        return (self.__base_speed + 200) * self.__speed_multiplier + 200 * random()