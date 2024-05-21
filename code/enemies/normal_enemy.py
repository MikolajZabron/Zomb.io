import pygame
from pygame import Vector2
from utilities.settings import *
from enemies.enemy import Enemy


class RegularEnemy(Enemy):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, image=ENEMY_TEMPLATE_IMAGE):
        super().__init__(groups, position, speed, health, attack_power, image)

    def calculate_movement(self, player_pos: Vector2):
        direction_vector = pygame.math.Vector2(player_pos.x - self.rect.x,
                                               player_pos.y - self.rect.y)
        if direction_vector.length() > 0:
            direction_vector.normalize()
            direction_vector.scale_to_length(self.speed)
            self.movement_direction = direction_vector

    def check_collision(self, player, structures):
        if pygame.sprite.collide_rect(self, player):
            player.take_damage(self.attack_power)

    def movement(self):
        self.rect.move_ip(self.movement_direction)

    def draw(self):
        self.screen.blit(self.image, self.rect)
