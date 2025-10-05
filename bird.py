import pygame
from img_wrapper import ImgWrapper

class Bird:
    __fps: float
    __fpa: int
    __frame_id: int

    # центр нижней стороны объекта
    __x: float
    __y: float

    __speed_ppf: float  # pixels per frame

    __imgs: tuple[ImgWrapper, ImgWrapper]
    __img_id: int

    __collider: pygame.Rect

    def __init__(
            self,
            fps: float,
            x: float,
            y: float,
            speed: float,                       # pixels per second
            animation_duration: float = 0.2,
    ):
        self.__fps = fps

        self.__x = x
        self.__y = y

        self.__init_imgs()
        self.__update_img_position()
        self.__update_collider()

        self.__speed_ppf = speed / self.__fps
        self.__fpa = max(1, round(animation_duration * self.__fps))
        self.__frame_id = 0

    def __init_imgs(self):
        """Загружает изображения"""
        directory = "./img/bird"
        self.__imgs = (
            ImgWrapper(0, 0, directory, "wing_up"),
            ImgWrapper(0, 0, directory, "wing_down"),
        )
        self.__img_id = 0

    def __switch_img(self):
        """Меняет изображение на следующее для данного состояния (циклично)"""
        self.__img_id = (self.__img_id + 1) % len(self.__imgs)

    def __update_collider(self):
        """
        Обновляет положение и размеры хит бокса
        (пересоздает на основе положения и размеров картинки)
        """
        self.__collider = self.__img.collider

    def __update_img_position(self):
        """Обновляет координаты для отрисовки актуальному изображению"""
        position = self.__img_position
        self.__img.x = position[0]
        self.__img.y = position[1]

    def before_render(self):
        """Предобработка фрейма (подготовка к отрисовке, обновление хит бокса)"""
        self.__x -= self.__speed_ppf
        self.__update_img_position()
        self.__update_collider()

    def after_render(self):
        """Постобработка фрейма (подготовка к следующему)"""
        # смена картинки с поправкой на длительность анимации
        self.__frame_id += 1
        if self.__frame_id % self.__fpa == 0:
            self.__switch_img()
            if self.__frame_id >= 1_000:
                self.__frame_id = 0

    def blit(self, surface: pygame.Surface):
        """Публикует актуальное изображение на поверхности"""
        self.__img.blit(surface)

    @property
    def is_outsider(self) -> bool:
        return self.__x + self.__img.width / 2 <= 0

    @property
    def __img_position(self) -> tuple[float, float]:
        """Позиция для отрисовки актуального изображения (левый верхний угол)"""
        return self.__x - self.__img.width / 2, self.__y - self.__img.height

    @property
    def __img(self) -> ImgWrapper:
        return self.__imgs[self.__img_id]

    @property
    def collider(self) -> pygame.Rect:
        return self.__collider