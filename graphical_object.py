from pygame.sprite import Sprite

import settings


class Object(Sprite):

    def __init__(self, game):
        super().__init__()

        # Game screen and settings initialization
        self.screen = game.screen
        self.settings = settings
        self.screen_rect = game.screen.get_rect()
