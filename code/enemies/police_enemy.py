import math

from pygame import Vector2

from enemies.zombie_projectile import Projectile  # Importing the Projectile class for enemy attacks
from utilities.settings import *  # Importing game settings
from enemies.enemy import Enemy  # Importing the Enemy base class


class PoliceEnemy(Enemy):
    """
    Represents a police enemy entity within the game.

    This class inherits from Enemy and defines behavior specific to police enemy entities, such as movement,
    collision detection, and attacking.

    Attributes:
        position (pygame.math.Vector2): The initial position of the police enemy.
        speed (int): The speed of the police enemy's movement.
        health (int): The current health points of the police enemy.
        attack_power (int): The attack power of the police enemy.
        animation_frames (list): List of frames for police enemy animation.
        movement_direction (pygame.math.Vector2): The direction of movement for the police enemy.
        attack_cooldown (int): The cooldown time between attacks.
        projectile_speed (int): The speed of the projectiles fired by the police enemy.
        last_attack_time (int): The time when the last attack was performed.
        min_distance (int): The minimum distance at which the police enemy engages with the player.

    Methods:
        __init__(groups, position, speed, health, attack_power, animation_frames): Constructor method for the PoliceEnemy class.
        calculate_movement(player_pos): Calculates movement direction towards the player.
        check_collision(player, structures): Checks collision with player and structures.
        movement(structures, borders, grid): Moves the police enemy while avoiding obstacles.
        collide_with_structures(structures): Handles collision with structures.
        collide_with_map_border(borders): Handles collision with map borders.
        avoid_obstacle(structure): Adjusts movement direction to avoid obstacles.
        attack(player_pos, groups): Performs an attack action towards the player.
    """

    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, animation_frames):
        """
        Constructor method for the PoliceEnemy class.

        Args:
            groups (pygame.sprite.AbstractGroup): The groups to which this police enemy belongs.
            position (pygame.math.Vector2): The initial position of the police enemy.
            speed (int): The speed of the police enemy's movement.
            health (int): The current health points of the police enemy.
            attack_power (int): The attack power of the police enemy.
            animation_frames (list): List of frames for police enemy animation.
        """
        super().__init__(groups, position, speed, health, attack_power, animation_frames)
        self.movement_direction = Vector2(0, 0)
        self.attack_cooldown = 3000
        self.projectile_speed = 5
        self.last_attack_time = 0
        self.min_distance = 200

    def calculate_movement(self, player_pos: Vector2):
        """
        Calculates movement direction towards the player and adjusts behavior based on distance.

        Args:
            player_pos (pygame.math.Vector2): The position of the player.
        """
        direction_vector = Vector2(player_pos.x - self.rect.centerx, player_pos.y - self.rect.centery)
        distance = math.sqrt((player_pos.x - self.rect.x) ** 2 + (player_pos.y - self.rect.y) ** 2)
        if distance > self.min_distance + 20:  # If player is far away, move towards player
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
        """
        Checks collision with player and structures and inflicts damage to player on collision.

        Args:
            player: The player object.
            structures: List of structures in the game.
        """
        if pygame.sprite.collide_mask(self, player):
            player.take_damage(self.attack_power)

    def movement(self, structures=None, borders=None, grid=None):
        """
        Moves the police enemy while avoiding obstacles.

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
        Handles collision with structures and adjusts movement direction to avoid obstacles.

        Args:
            structures: List of structures in the game.
        """
        for structure in structures:
            if pygame.sprite.collide_rect(self, structure):
                self.avoid_obstacle(structure)

    def collide_with_map_border(self, borders):
        """
        Handles collision with map borders and adjusts movement direction to avoid obstacles.

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

    def attack(self, player_pos: Vector2, groups):
        """
        Attack action towards the player.

        Args:
            player_pos (pygame.math.Vector2): The position of the player.
            groups: The groups to which the projectile belongs.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            direction_vector = Vector2(player_pos.x - self.rect.centerx, player_pos.y - self.rect.centery)
            if direction_vector.length() > 0:
                direction_vector.normalize()
            Projectile(self.rect.center, direction_vector, self.projectile_speed, self.attack_power, groups)
            self.last_attack_time = current_time
