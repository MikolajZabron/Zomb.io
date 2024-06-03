import math

from pygame import Vector2

from enemies.zombie_projectile import Projectile
from utilities.settings import *
from enemies.enemy import Enemy


class PoliceEnemy(Enemy):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, animation_frames,
                 image=ENEMY_TEMPLATE_IMAGE):
        super().__init__(groups, position, speed, health, attack_power, animation_frames, image)
        self.movement_direction = Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
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

    def movement(self, structures=None):
        self.old_x, self.old_y = self.rect.topleft
        self.rect.move_ip(self.movement_direction)
        if structures:
            self.collide_with_structures(structures)
        self.update_animation()

    def collide_with_structures(self, structures):
        for structure in structures:
            if pygame.sprite.collide_mask(self, structure):
                self.avoid_obstacle(structure)

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

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 1000 // self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame].convert_alpha()
            self.image = pygame.transform.scale(self.image, (120, 120))
            self.mask = pygame.mask.from_surface(self.image)
            self.last_update_time = current_time

    def attack(self, player_pos: Vector2, groups):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            direction_vector = Vector2(player_pos.x - self.rect.centerx, player_pos.y - self.rect.centery)
            if direction_vector.length() > 0:
                direction_vector.normalize()
            projectile = Projectile(self.rect.center, direction_vector, self.projectile_speed, self.attack_power,
                                    groups)
            self.last_attack_time = current_time