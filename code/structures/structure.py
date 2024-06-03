from utilities.graphical_object import Object
import pygame


class Structure(Object):
    def __init__(self, position, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)


class CollisionBoundary(Object):
    def __init__(self, pos, width, height, groups):
        super().__init__(groups)
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.image = pygame.Surface((width, height))
        self.image.set_alpha(0)


class Ground(Object):
    def __init__(self, position, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=position)
