from pygame import Vector2
from utilities.settings import *
from enemies.enemy import Enemy
import math


class RiotEnemy(Enemy):
    """
    Represents a riot enemy entity within the game.

    This class inherits from Enemy and defines behavior specific to riot enemy entities, such as movement,
    charging towards the player, and collision detection.

    Attributes:
        position (pygame.math.Vector2): The initial position of the riot enemy.
        speed (int): The speed of the riot enemy's movement.
        health (int): The current health points of the riot enemy.
        attack_power (int): The attack power of the riot enemy.
        animation_frames (list): List of frames for riot enemy animation.
        movement_direction (pygame.math.Vector2): The direction of movement for the riot enemy.
        charge_loading (bool): Flag indicating whether the riot enemy is loading its charge attack.
        charging (bool): Flag indicating whether the riot enemy is currently charging towards the player.
        charge_start_time (int): The time when the riot enemy started loading its charge attack.
        last_player_pos (pygame.math.Vector2): The position of the player when the riot enemy started charging.

    Methods:
        __init__(groups, position, speed, health, attack_power, animation_frames): Constructor method for the RiotEnemy class.
        calculate_movement(player_pos): Calculates movement direction towards the player and handles charging behavior.
        check_collision(player, structures): Checks collision with player and structures.
        movement(structures, borders, grid): Moves the riot enemy while avoiding obstacles.
        collide_with_structures(structures): Handles collision with structures.
        collide_with_map_border(borders): Handles collision with map borders.
        avoid_obstacle(structure): Adjusts movement direction to avoid obstacles.
    """

    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, animation_frames):
        """
        Constructor method for the RiotEnemy class.

        Args:
            groups (pygame.sprite.AbstractGroup): The groups to which this riot enemy belongs.
            position (pygame.math.Vector2): The initial position of the riot enemy.
            speed (int): The speed of the riot enemy's movement.
            health (int): The current health points of the riot enemy.
            attack_power (int): The attack power of the riot enemy.
            animation_frames (list): List of frames for riot enemy animation.
        """
        super().__init__(groups, position, speed, health, attack_power, animation_frames)
        self.movement_direction = Vector2(0, 0)
        self.charge_loading = False
        self.charging = False
        self.charge_start_time = 0
        self.last_player_pos = None

    def calculate_movement(self, player_pos: Vector2):
        """
        Calculates movement direction towards the player and handles charging behavior.

        Args:
            player_pos (pygame.math.Vector2): The position of the player.
        """
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
        Moves the riot enemy while avoiding obstacles.

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
            self.movement_direction.scale_to_length(self.speed)

        self.rect.move_ip(self.movement_direction)
