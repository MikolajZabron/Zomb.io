from utilities.graphical_object import Object
from pygame.math import Vector2
from utilities.settings import *


class Enemy(Object):
    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, animation_frames):
        super().__init__(groups)
        self.animation_frames = animation_frames
        self.position: Vector2 = position
        self.screen = pygame.display.get_surface()
        self.image = self.animation_frames[0].convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.old_x = 0
        self.old_y = 0
        self.last_shot_time = 0

        # Basic Statistics
        self.health: int = health
        self.speed: int = speed
        self.attack_power: int = attack_power
        self.exp: int = 10

        self.movement_direction: pygame.math.Vector2 = pygame.math.Vector2()

        # Animation stuff
        self.frame_rate = 10
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.tile_size = 32

    def update(self):
        pass

    def calculate_movement(self, player_pos: Vector2):
        pass

    def movement(self):
        pass

    def damage_player(self):
        pass

    def check_collision(self, player, structures):
        pass

    def take_damage(self, amount, player):
        self.health -= amount
        if self.health <= 0:
            self.kill()
            player.gain_experience(self.exp)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 1000 // self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame].convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.mask = pygame.mask.from_surface(self.image)
            self.last_update_time = current_time

    def separate_from_other_enemies(self, grid):
        separation_distance = 15
        separation_force = Vector2(0, 0)
        tile_x, tile_y = self.tile_position(self.rect.center)

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                cell = (tile_x + dx, tile_y + dy)
                if cell in grid:
                    for enemy in grid[cell]:
                        if enemy is not self:
                            distance = Vector2(self.rect.center) - Vector2(enemy.rect.center)
                            if 0 < distance.length() < separation_distance:
                                separation_force += distance.normalize() / distance.length()

        if separation_force.length() > 0:
            separation_force.normalize()
            separation_force.scale_to_length(self.speed)
            self.rect.move_ip(separation_force)

    def tile_position(self, position):
        return int(position[0] // self.tile_size), int(position[1] // self.tile_size)
