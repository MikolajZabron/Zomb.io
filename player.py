import settings
from graphical_object import Object


class Player(Object):

    def __init__(self, game):
        super().__init__(game)
        self.image = settings.PLAYER_IMAGE
        self.rect = self.image.get_rect()

        self.screen_rect = game.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right:
            self.x += settings.PLAYER_SPEED
        if self.moving_left:
            self.x -= settings.PLAYER_SPEED
        if self.moving_up:
            self.y -= settings.PLAYER_SPEED
        if self.moving_down:
            self.y += settings.PLAYER_SPEED

        self.rect.x = self.x
        self.rect.y = self.y

    def blit_player(self):
        self.screen.blit(self.image, self.rect)
