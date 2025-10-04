import pygame
from utils import load_img

class ImgWrapper:
    img: pygame.Surface
    x: float
    y: float

    def __init__(self, x: float, y: float, directory: str, filename: str, extension: str = 'png'):
        self.x = x
        self.y = y
        self.load(directory, filename, extension)

    def load(self, directory: str, filename: str, extension: str = 'png'):
        """Загружает изображение"""
        self.img = load_img(directory, filename, extension)

    def blit(self, surface: pygame.Surface):
        """Публикует картинку на поверхность по координатам (topleft)"""
        surface.blit(self.img, self.position)

    @property
    def width(self) -> float:
        return self.img.get_width()

    @property
    def height(self) -> float:
        return self.img.get_height()

    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y

    @position.setter
    def position(self, value: tuple[float, float]):
        self.x = value[0]
        self.y = value[1]

    @property
    def collider(self) -> pygame.Rect:
        """Создает Rect по размеру и координатам картинки (topleft)"""
        return self.img.get_rect(topleft=self.position)