from pygame import Vector2
from utilities.settings import *
from enemies.enemy import Enemy
import math


class RiotEnemy(Enemy):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, animation_frames,
                 image=ENEMY_TEMPLATE_IMAGE):
        super().__init__(groups, position, speed, health, attack_power, animation_frames, image)
        self.movement_direction = Vector2(0, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.charge_loading = False
        self.charging = False
        self.charge_start_time = 0
        self.last_player_pos = None

    def calculate_movement(self, player_pos: Vector2):
        if not self.charging and not self.charge_loading:
            direction_vector = pygame.math.Vector2(player_pos.x - self.rect.x,
                                                   player_pos.y - self.rect.y)
            if direction_vector.length() > 0:
                direction_vector.normalize()
                direction_vector.scale_to_length(self.speed)
                self.movement_direction = direction_vector

            distance_to_player = math.sqrt((player_pos.x - self.rect.x) ** 2 + (player_pos.y - self.rect.y) ** 2)
            if distance_to_player < 300:
                self.charge_start_time = pygame.time.get_ticks()
                self.charge_loading = True
        elif self.charging:
            direction_vector = pygame.math.Vector2(self.last_player_pos.x - self.rect.x,
                                                   self.last_player_pos.y - self.rect.y)
            if direction_vector.length() > 0:
                direction_vector.normalize()
                direction_vector.scale_to_length(self.speed * 3)
                self.movement_direction = direction_vector
            distance_to_point = math.sqrt((self.last_player_pos.x - self.rect.x) ** 2 +
                                          (self.last_player_pos.y - self.rect.y) ** 2)
            if distance_to_point < 20:
                self.movement_direction = pygame.math.Vector2(0, 0)
                self.charging = False
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.charge_start_time > 1500:
                self.charging = True
                self.charge_loading = False
                self.last_player_pos = player_pos
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
