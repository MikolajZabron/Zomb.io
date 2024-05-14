from utilities.graphical_object import Object
from pygame.math import Vector2
from utilities.settings import *


class Enemy(Object):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, image=ENEMY_TEMPLATE_IMAGE):
        super().__init__(groups)
        self.position: Vector2 = position
        self.screen = pygame.display.get_surface()
        self.image = image
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.rect = self.image.get_rect(center=position)

        # Basic Statistics
        self.health: int = health
        self.speed: int = speed
        self.attack_power: int = attack_power

    def update(self):
        pass

    def draw(self):
        pass

    def move(self, player_pos: Vector2):
        pass

    def damage_player(self):
        pass

    def check_collision(self, player):
        pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
