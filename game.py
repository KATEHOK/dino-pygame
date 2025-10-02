import pygame
from utils import load_img

class Game:
    __is_running: bool
    __fps: float
    __screen_size: tuple[float, float]

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

            for event in pygame.event.get():
                self.__handle_event(event)


    def __before_render(self):
        """Действия с объектами до отрисовки"""
        ...


    def __render(self):
        """Отрисовка объектов"""
        self.screen.fill((255, 255, 255))
        pygame.display.update()


    def __after_render(self):
        """Действия с объектами после отрисовки"""
        ...


    def __handle_event(self, event):
        """Обработка событий"""
        if event.type == pygame.QUIT:
            self.__quit()


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