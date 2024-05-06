from utilities.settings import *


class World:
    """
    World-class to represent a game world
    """

    def __init__(self):
        self.surface = pygame.display.get_surface()

    def start(self):
        self.surface.fill('black')
