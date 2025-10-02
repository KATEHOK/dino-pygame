import pygame
import os

def load_img(directory: str, filename: str, extension: str = "png") -> pygame.Surface:
    try:
        file_path = os.path.join(directory, f"{filename}.{extension}")
        image = pygame.image.load(file_path)
        return image.convert_alpha()
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error loading image {filename}.{extension}: {e}")
        raise