import pygame
from pygame import Vector2
from utilities.settings import *
from enemies.enemy import Enemy


class RegularEnemy(Enemy):
    """
    Represents a regular enemy entity within the game.

    This class inherits from Enemy and defines behavior specific to regular enemy entities, such as movement,
    collision detection, and obstacle avoidance.

    Attributes:
        position (pygame.math.Vector2): The initial position of the regular enemy.
        speed (int): The speed of the regular enemy's movement.
        health (int): The current health points of the regular enemy.
        attack_power (int): The attack power of the regular enemy.
        animation_frames (list): List of frames for regular enemy animation.
        image (pygame.Surface): The image representing the regular enemy (defaults to ENEMY_TEMPLATE_IMAGE).

    Methods:
        __init__(groups, position, speed, health, attack_power, animation_frames, image): Constructor method for the RegularEnemy class.
        calculate_movement(player_pos): Calculates movement direction towards the player.
        check_collision(player, structures): Checks collision with player and structures.
        movement(structures, borders, grid): Moves the regular enemy while avoiding obstacles.
        collide_with_structures(structures): Handles collision with structures.
        collide_with_map_border(borders): Handles collision with map borders.
        avoid_obstacle(structure): Adjusts movement direction to avoid obstacles.
    """

    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, animation_frames,
                 image=ENEMY_TEMPLATE_IMAGE):
        """
        Constructor method for the RegularEnemy class.

        Args:
            groups (pygame.sprite.AbstractGroup): The groups to which this regular enemy belongs.
            position (pygame.math.Vector2): The initial position of the regular enemy.
            speed (int): The speed of the regular enemy's movement.
            health (int): The current health points of the regular enemy.
            attack_power (int): The attack power of the regular enemy.
            animation_frames (list): List of frames for regular enemy animation.
            image (pygame.Surface, optional): The image representing the regular enemy (defaults to ENEMY_TEMPLATE_IMAGE).
        """
        super().__init__(groups, position, speed, health, attack_power, animation_frames)
        self.movement_direction = Vector2(0, 0)
        self.tile_size = 32

    def calculate_movement(self, player_pos: Vector2):
        """
        Calculates movement direction towards the player.

        Args:
            player_pos (pygame.math.Vector2): The position of the player.
        """
        direction_vector = pygame.math.Vector2(player_pos.x - self.rect.x,
                                               player_pos.y - self.rect.y)
        if direction_vector.length() > 0:
            direction_vector.normalize()
            direction_vector.scale_to_length(self.speed)
            self.movement_direction = direction_vector

    def check_collision(self, player, structures):
        """
        Checks collision with player and structures.

        Args:
            player: The player object.
            structures: List of structures in the game.
        """
        if pygame.sprite.collide_mask(self, player):
            player.take_damage(self.attack_power)

    def movement(self, structures=None, borders=None, grid=None):
        """
        Moves the regular enemy while avoiding obstacles.

        Args:
            structures: List of structures in the game.
            borders: List of map borders.
            grid: Grid containing positions of other enemies.
        """
        self.old_x, self.old_y = self.rect.center
        self.rect.move_ip(self.movement_direction)
        if borders:
            self.collide_with_map_border(borders)
        if structures:
            self.collide_with_structures(structures)
        if grid:
            self.separate_from_other_enemies(grid)
        self.update_animation()

    def collide_with_structures(self, structures):
        """
        Handles collision with structures.

        Args:
            structures: List of structures in the game.
        """
        for structure in structures:
            if pygame.sprite.collide_rect(self, structure):
                self.avoid_obstacle(structure)

    def collide_with_map_border(self, borders):
        """
        Handles collision with map borders.

        Args:
            borders: List of map borders.
        """
        for border in borders:
            if pygame.sprite.collide_rect(self, border):
                self.avoid_obstacle(border)

    def avoid_obstacle(self, structure):
        """
        Adjusts movement direction to avoid obstacles.

        Args:
            structure: The obstacle structure to avoid.
        """
        avoid_vector = Vector2(self.rect.center) - Vector2(structure.rect.center)
        if avoid_vector.length() > 0:
            avoid_vector.normalize()
            avoid_vector.scale_to_length(self.speed)

        self.movement_direction += avoid_vector
        if self.movement_direction.length() > 0:
            self.movement_direction.normalize()
            if self.movement_direction.length() > 0:
                self.movement_direction.scale_to_length(self.speed)

        self.rect.move_ip(self.movement_direction)
