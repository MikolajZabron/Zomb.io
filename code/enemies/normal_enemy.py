import pygame
from pygame import Vector2
from utilities.settings import *
from enemies.enemy import Enemy


class RegularEnemy(Enemy):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, image=ENEMY_TEMPLATE_IMAGE):
        super().__init__(groups, position, speed, health, attack_power, image)
        self.movement_direction = Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def calculate_movement(self, player_pos: Vector2):
        direction_vector = pygame.math.Vector2(player_pos.x - self.rect.x,
                                               player_pos.y - self.rect.y)
        if direction_vector.length() > 0:
            direction_vector.normalize()
            direction_vector.scale_to_length(self.speed)
            self.movement_direction = direction_vector

    def check_collision(self, player, structures):
        if pygame.sprite.collide_mask(self, player):
            player.take_damage(self.attack_power)

    def movement(self, structures=None):
        self.old_x, self.old_y = self.rect.topleft
        self.rect.move_ip(self.movement_direction)
        if structures:
            self.collide_with_structures(structures)

    def collide_with_structures(self, structures):
        for structure in structures:
            if pygame.sprite.collide_mask(self, structure):
                self.avoid_obstacle(structure)

    def avoid_obstacle(self, structure):
        # Calculate a vector away from the obstacle
        avoid_vector = Vector2(self.rect.center) - Vector2(structure.rect.center)
        avoid_vector.normalize()
        avoid_vector.scale_to_length(self.speed)

        # Combine the current movement direction with the avoid vector
        self.movement_direction += avoid_vector
        self.movement_direction.normalize()
        self.movement_direction.scale_to_length(self.speed)

        # Move the enemy based on the new movement direction
        self.rect.move_ip(self.movement_direction)

    def draw(self):
        self.screen.blit(self.image, self.rect)