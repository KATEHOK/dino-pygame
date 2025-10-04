import pygame
from img_wrapper import ImgWrapper

class Bg:
    __left_img: ImgWrapper
    __right_img: ImgWrapper
    __screen_size: tuple[float, float]
    __speed_ppf: float                  # pixels per frame
    __x: float

    def __init__(
            self,
            screen_size: tuple[float, float],
            fps: float,
            speed: float,               # pixels per second
            img_directory: str = "img",
            img_filename: str = "bg",
            img_extension: str = "jpg",
    ):
        self.__x = 0
        self.__left_img = ImgWrapper(0, 0, img_directory, img_filename, img_extension)
        self.__right_img = ImgWrapper(self.__left_img.width, 0, img_directory, img_filename, img_extension)
        self.__screen_size = screen_size
        self.__speed_ppf = speed / fps

    def speedup(self, percent: float = 10):
        """Увеличивает скорость"""
        self.__speed_ppf *= (1 + percent)

    def blit(self, surface: pygame.Surface):
        """Публикует изображения фона на поверхности"""
        self.__left_img.blit(surface)
        self.__right_img.blit(surface)

    def before_render(self):
        """Сдвигает фоновые изображения"""
        self.__x = (self.__x - self.__speed_ppf) % -self.__left_img.width
        self.__left_img.x = self.__x
        self.__right_img.x = self.__x + self.__left_img.width
