from utilities.settings import *
from utilities.graphical_object import Object


class BulletTemplate(Object):
    def __init__(self, position, destination, groups):
        super().__init__(groups)
        self.image = BULLET_TEMPLATE_IMAGE.convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=position)
        self.screen = pygame.display.get_surface()
        self.destination = destination
        self.direction = pygame.math.Vector2()
        self.speed = BULLET_SPEED

    def collision(self, group, damage, player):
        for enemy in pygame.sprite.spritecollide(self, group, False):
            enemy.take_damage(damage, player)
            self.kill()

    def update(self):  # temporary to change
        direction = pygame.math.Vector2(self.destination[0] - self.rect.centerx,
                                        self.destination[1] - self.rect.centery)
        direction.normalize_ip()
        self.rect.move_ip(direction * self.speed)

        if (direction.x > 0 and self.rect.centerx >= self.destination[0]) or \
                (direction.x < 0 and self.rect.centerx <= self.destination[0]) or \
                (direction.y > 0 and self.rect.centery >= self.destination[1]) or \
                (direction.y < 0 and self.rect.centery <= self.destination[1]):
            self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)
