import pygame
from utils import load_img
from dino import Dino

class Game:
    __is_running: bool
    __fps: float
    __screen_size: tuple[float, float]
    __dino: Dino
    __plane_y: float

    def __init__(
            self,
            fps: float = 60,
            screen_size: tuple[float, float] = (1200, 600)
    ):
        self.__is_running = False
        self.__fps = fps
        self.__screen_size = screen_size

        pygame.init()
        self.__clock = pygame.time.Clock()
        self.__init_screen()

        self.__plane_y = self.__screen_size[1] * 0.75
        self.__dino = Dino(
            fps=self.__fps,
            x=self.__screen_size[0] * 0.2, y=self.__plane_y,
            jump_height=self.__screen_size[1] * 0.4, jump_duration=0.75,
            animation_duration=0.1
        )


    def start(self):
        """Запуск игры"""
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


    def __before_render(self):
        """Действия с объектами до отрисовки"""
        self.__dino.before_render()


    def __render(self):
        """Отрисовка объектов"""
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.__dino.img, self.__dino.img_position)
        pygame.display.update()


    def __after_render(self):
        """Действия с объектами после отрисовки"""
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