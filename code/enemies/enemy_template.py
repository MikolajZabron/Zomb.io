from utilities.settings import *
from enemies.enemy import Enemy


class EnemyTemplate(Enemy):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = ENEMY_TEMPLATE_IMAGE.convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.rect = self.image.get_rect(center=position)
        self.screen = pygame.display.get_surface()
        self.health = ENEMY_TEMPLATE_HEALTH

    def draw(self):
        self.screen.blit(self.image, self.rect)
