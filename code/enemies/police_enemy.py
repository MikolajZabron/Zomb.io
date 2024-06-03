import math

from pygame import Vector2

from enemies.zombie_projectile import Projectile
from utilities.settings import *
from enemies.enemy import Enemy


class PoliceEnemy(Enemy):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, animation_frames):
        super().__init__(groups, position, speed, health, attack_power, animation_frames)
        self.movement_direction = Vector2(0, 0)
        self.attack_cooldown = 3000
        self.projectile_speed = 5
        self.last_attack_time = 0
        self.min_distance = 200

    def calculate_movement(self, player_pos: Vector2):
        direction_vector = Vector2(player_pos.x - self.rect.centerx, player_pos.y - self.rect.centery)
        distance = math.sqrt((player_pos.x - self.rect.x) ** 2 + (player_pos.y - self.rect.y) ** 2)
        if distance > self.min_distance + 20:
            direction_vector.normalize()
            direction_vector.scale_to_length(self.speed)
            self.movement_direction = direction_vector
        elif distance < self.min_distance:
            direction_vector = -direction_vector
            direction_vector.normalize()
            direction_vector.scale_to_length(self.speed)
            self.movement_direction = direction_vector
        else:
            self.movement_direction = pygame.math.Vector2(0, 0)

    def check_collision(self, player, structures):
        if pygame.sprite.collide_mask(self, player):
            player.take_damage(self.attack_power)

    def movement(self, structures=None, borders=None):
        self.old_x, self.old_y = self.rect.center
        self.rect.move_ip(self.movement_direction)
        if borders:
            self.collide_with_map_border(borders)
        if structures:
            self.collide_with_structures(structures)
        self.update_animation()

    def collide_with_structures(self, structures):
        for structure in structures:
            if pygame.sprite.collide_rect(self, structure):
                self.avoid_obstacle(structure)

    def collide_with_map_border(self, borders):
        for border in borders:
            if pygame.sprite.collide_rect(self, border):
                self.avoid_obstacle(border)

    def avoid_obstacle(self, structure):
        avoid_vector = Vector2(self.rect.center) - Vector2(structure.rect.center)
        if avoid_vector.length() > 0:
            avoid_vector.normalize()
            avoid_vector.scale_to_length(self.speed)

        self.movement_direction += avoid_vector
        if self.movement_direction.length() > 0:
            self.movement_direction.normalize()
            self.movement_direction.scale_to_length(self.speed)

        self.rect.move_ip(self.movement_direction)

    def attack(self, player_pos: Vector2, groups):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            direction_vector = Vector2(player_pos.x - self.rect.centerx, player_pos.y - self.rect.centery)
            if direction_vector.length() > 0:
                direction_vector.normalize()
            Projectile(self.rect.center, direction_vector, self.projectile_speed, self.attack_power,
                                    groups)
            self.last_attack_time = current_time
