from utilities.settings import *
from utilities.graphical_object import Object


class Melee(Object):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = MELEE_TEMPLATE
        self.image = pygame.transform.scale(self.image, (100, 5))
        self.rect = self.image.get_rect(center=position)
        self.screen = pygame.display.get_surface()
        self.direction = pygame.math.Vector2()
        self.dealt_damage = False

    def deal_damage(self):
        self.dealt_damage = True
        self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)
