from settings import *
from graphical_object import Object


class Player(Object):

    def __init__(self, position, group):
        super().__init__(group)
        self.image = PLAYER_IMAGE.convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 75))
        self.rect = self.image.get_rect(center=position)
        self.screen = pygame.display.get_surface()
        self.direction = pygame.math.Vector2()

        self.speed = PLAYER_SPEED

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self):

        self.input()
        self.rect.center += self.direction * self.speed

    def blit_player(self):
        self.screen.blit(self.image, self.rect)
