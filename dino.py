import pygame
from utils import load_img

class Dino:
    # фреймов в секунду
    __fps: float
    # фреймов на анимацию
    __fpa: int
    __frame_id: int

    __collider: pygame.Rect

    __is_jumping: bool
    __is_ducking: bool

    __imgs: dict[str, tuple[pygame.Surface, ...]]
    __img_id: int

    # центр нижней стороны объекта (ноги динозавра)
    __x: float
    __y: float

    # Прыжок - по параболе из irl физики:
    # y(t) = B + 4H/T [(t^2)/T - t]
    # y - ордината
    # t - абсцисса (время в секундах)
    # B - ордината в момент начала прыжка
    # H - высота прыжка
    # T - длительность прыжка (время в секундах)

    # ордината в момент до начала прыжка
    __jump_base_y: float
    # высота прыжка
    __jump_height: float
    # продолжительность прыжка (в секундах)
    __jump_duration: float
    # 4H/T
    __jump_multiplier: float

    # продолжительность прыжка (в фреймах - целое, округляется)
    __jump_frames: int
    # индекс фрейма прыжка
    __jump_frame_id: int

    def __init__(
            self,
            fps: float,
            x: float,
            y: float,
            jump_height: float = 250,
            jump_duration: float = 1,
            animation_duration: float = 0.1
    ):
        self.__fps = fps

        self.__x = x
        self.__y = y

        self.__jump_height = jump_height
        self.__jump_duration = jump_duration

        self.__jump_frames = round(self.__jump_duration * self.__fps)
        self.__jump_frame_id = self.__jump_frames

        # 4H/T
        self.__jump_multiplier = 4 * self.__jump_height / self.__jump_frames

        self.__init_states()
        self.__init_imgs()
        self.__init_collider()

        self.__fpa = max(1, round(animation_duration * self.__fps))
        self.__frame_id = 0


    def before_render(self):
        """Предобработка фрейма (подготовка к отрисовке, обновление хит бокса)"""
        if self.__is_jumping:
                self.__jumping()
        self.__update_collider()

    def after_render(self):
        """Постобработка фрейма (подготовка к следующему)"""
        # смена картинки с поправкой на длительность анимации
        self.__frame_id += 1
        if self.__frame_id % self.__fpa == 0:
            self.__switch_img()
            if self.__frame_id >= 1_000:
                self.__frame_id = 0

    def duck(self):
        """Начало приседания"""
        if not self.__is_jumping:
            self.__is_ducking = True
            self.__reset_img()

    def unduck(self):
        """Завершение приседания"""
        self.__unduck()
        self.__reset_img()

    def jump(self):
        """Запуск начала прыжка"""
        if not self.__is_jumping:
            self.__unduck()
            self.__jump_base_y = self.__y
            self.__jump_frame_id = 0
            self.__is_jumping = True
            self.__reset_img()


    def __init_collider(self):
        """Инициализирует хит бокс"""
        self.__update_collider()

    def __init_states(self):
        """Инициализирует состояния"""
        self.__is_jumping = False
        self.__is_ducking = False

    def __init_imgs(self):
        """Загружает изображения"""
        directory = "./img/dino/base"
        self.__imgs = {
            'running': (
                load_img(directory, "left_step"),
                load_img(directory, "right_step"),
            ),
            'jumping': (
                load_img(directory, "jump"),
            ),
            'ducking': (
                load_img(directory, "down_left_step"),
                load_img(directory, "down_right_step"),
            )
        }
        self.__img_id = 0

    def __update_collider(self):
        """
        Обновляет положение и размеры хит бокса
        (пересоздает на основе положения и размеров картинки)
        """
        self.__collider = self.img.get_rect(topleft=self.img_position)

    def __reset_img(self):
        """Сбрасывает текущее изображение до первого для данного состояния"""
        self.__img_id = 0

    def __jumping(self):
        """Обработка прыжка в текущем фрейме"""
        if self.__jump_frame_id < self.__jump_frames:
            # продолжаем прыжок
            # y(t) = B + 4H/T [(t^2)/T - t]
            self.__y = (self.__jump_base_y + self.__jump_multiplier *
                        (self.__jump_frame_id ** 2 / self.__jump_frames - self.__jump_frame_id))
            self.__jump_frame_id += 1
        else:
            # допрыгались
            self.__y = self.__jump_base_y
            self.__is_jumping = False

    def __switch_img(self):
        """Меняет изображение на следующее для данного состояния (циклично)"""
        self.__img_id = (self.__img_id + 1) % len(self.__get_imgs)

    def __unduck(self):
        """Завершение приседания (не сбрасывает картинку)"""
        self.__is_ducking = False


    @property
    def collider(self) -> pygame.Rect:
        """Актуальный хит бокс"""
        return self.__collider

    @property
    def img_position(self) -> tuple[float, float]:
        """Позиция для отрисовки актуального изображения (левый верхний угол)"""
        return self.__x - self.img.get_width() / 2, self.__y - self.img.get_height()

    @property
    def img(self) -> pygame.Surface:
        """Актуальное изображение"""
        return self.__get_imgs[self.__img_id]

    @property
    def __get_imgs(self) -> tuple[pygame.Surface, ...]:
        """Изображения для актуального состояния"""
        if self.__is_jumping:
            return self.__imgs['jumping']
        elif self.__is_ducking:
            return  self.__imgs['ducking']
        else:
            return  self.__imgs['running']