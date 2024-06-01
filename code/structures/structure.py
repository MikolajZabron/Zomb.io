from utilities.graphical_object import Object
import pygame


class Structure(Object):
    def __init__(self, position, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)


class Tile(Object):
    def __init__(self, position, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=position)
