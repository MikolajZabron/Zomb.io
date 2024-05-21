import pygame

from utilities.graphical_object import Object
from pygame.math import Vector2
from utilities.settings import *


class Enemy(Object):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, image=ENEMY_TEMPLATE_IMAGE):
        super().__init__(groups)
        self.position: Vector2 = position
        self.screen = pygame.display.get_surface()
        self.image = image
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(center=position)

        # Basic Statistics
        self.health: int = health
        self.speed: int = speed
        self.attack_power: int = attack_power

        self.movement_direction: pygame.math.Vector2 = pygame.math.Vector2()

    def update(self):
        pass

    def draw(self):
        pass

    def calculate_movement(self, player_pos: Vector2):
        pass

    def movement(self):
        pass

    def damage_player(self):
        pass

    def check_collision(self, player, structures):
        pass

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
