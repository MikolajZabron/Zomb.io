import pygame.sprite


class Object(pygame.sprite.Sprite):
    """
    Abstract class, base for all graphical objects in the game
    """

    def __init__(self, group):
        super().__init__(group)
