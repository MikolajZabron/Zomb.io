import pygame
from pygame.math import Vector2

from utilities.graphical_object import Object
from utilities.settings import BULLET_TEMPLATE_IMAGE


class Projectile(Object):
    def __init__(self, position, direction, speed, damage, groups):
        super().__init__(groups)
        self.image = BULLET_TEMPLATE_IMAGE.convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=position)
        self.direction = direction.normalize()
        self.speed = speed
        self.damage = damage
        self.screen = pygame.display.get_surface()
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 4000
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.lifespan:
            self.kill()
        if not self.rect.colliderect(pygame.display.get_surface().get_rect()):
            self.kill()

    def check_collision(self, player):
        if pygame.sprite.collide_mask(self, player):
            player.take_damage(self.damage)
            self.kill()
