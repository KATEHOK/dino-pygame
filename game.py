import pygame

class Game:
    __is_running: bool = False

    def __init__(self):
        print("Hello from Game.__init__")
        pygame.init()

        self.__init_screen()


    def start(self):
        """Запуск игры"""
        print("Hello from Game.start")
        self.__is_running = True
        self.__loop()

    def __loop(self):
        """Игровой цикл"""
        print("Hello from Game.__loop")
        while self.__is_running:

            for event in pygame.event.get():
                self.__handle_event(event)


    def __handle_event(self, event):
        """Обработка событий"""
        print("Hello from Game.__check_event")
        if event.type == pygame.QUIT:
            self.__quit()


    def __quit(self):
        """Завершение игры"""
        print("Hello from Game.__quit")
        self.__is_running = False
        pygame.quit()
        self.__loop()


    def __init_screen(
            self,
            screen_size: tuple[float, float] = (1200, 600),
            caption: str = "Dino",
            icon_path: str = "./img/icon.png"
    ):
        """Инициализация игрового окна"""
        print("Hello from Game.__init_screen")
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)
        pygame.display.set_icon(pygame.image.load(icon_path))