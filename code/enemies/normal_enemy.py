import pygame
from pygame import Vector2
from utilities.settings import *
from enemies.enemy import Enemy


class RegularEnemy(Enemy):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, image=ENEMY_TEMPLATE_IMAGE):
        super().__init__(groups, position, speed, health, attack_power, image)

    def move(self, player_pos: Vector2):
        direction_vector = player_pos - self.position
        direction_vector.normalize_ip()
        direction_vector.scale_to_length(self.speed)
        self.rect.move_ip(direction_vector)

    def check_collision(self, player):
        if pygame.sprite.collide_rect(self.rect, player.rect):
            player.take_damage(self.attack_power)

    def draw(self):
        self.screen.blit(self.image, self.rect)
