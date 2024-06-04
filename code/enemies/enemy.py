from utilities.graphical_object import Object
from pygame.math import Vector2
from utilities.settings import *


class Enemy(Object):
    """
    Represents an enemy entity within the game.

    This class inherits from Object and defines behavior specific to enemy entities, such as movement, attacking,
    and interactions with other game objects.

    Attributes:
        position (pygame.math.Vector2): The initial position of the enemy.
        speed (int): The speed of the enemy's movement.
        health (int): The current health points of the enemy.
        attack_power (int): The attack power of the enemy.
        animation_frames (list): List of frames for enemy animation.

    Methods:
        __init__(groups, position, speed, health, attack_power, animation_frames): Constructor method for Enemy class.
        update(): Updates the state of the enemy.
        calculate_movement(player_pos): Calculates movement direction towards the player.
        movement(): Moves the enemy based on calculated movement direction.
        damage_player(): Inflicts damage to the player.
        check_collision(player, structures): Checks collision with player and structures.
        take_damage(amount, player): Reduces enemy health when attacked by the player.
        draw(): Draws the enemy on the screen.
        update_animation(): Updates the animation frames of the enemy.
        separate_from_other_enemies(grid): Moves the enemy away from nearby enemies to avoid overlapping.
        tile_position(position): Returns the tile position of the given pixel position.
    """

    def __init__(self, groups, position: Vector2, speed, health: int, attack_power: int, animation_frames):
        """
        Constructor method for the Enemy class.

        Args:
            groups (pygame.sprite.AbstractGroup): The groups to which this enemy belongs.
            position (pygame.math.Vector2): The initial position of the enemy.
            speed (int): The speed of the enemy's movement.
            health (int): The current health points of the enemy.
            attack_power (int): The attack power of the enemy.
            animation_frames (list): List of frames for enemy animation.
        """
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
        """Updates the state of the enemy."""
        pass

    def calculate_movement(self, player_pos: Vector2):
        """Calculates movement direction towards the player."""
        pass

    def movement(self):
        """Moves the enemy based on calculated movement direction."""
        pass

    def damage_player(self):
        """Inflicts damage to the player."""
        pass

    def check_collision(self, player, structures):
        """Checks collision with player and structures."""
        pass

    def take_damage(self, amount, player):
        """
        Reduces enemy health when attacked by the player.

        Args:
            amount (int): The amount of damage inflicted.
            player: The player object inflicting the damage.
        """
        self.health -= amount
        if self.health <= 0:
            self.kill()
            player.gain_experience(self.exp)

    def draw(self):
        """Draws the enemy on the screen."""
        self.screen.blit(self.image, self.rect)

    def update_animation(self):
        """Updates the animation frames of the enemy."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 1000 // self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.image = self.animation_frames[self.current_frame].convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
            self.mask = pygame.mask.from_surface(self.image)
            self.last_update_time = current_time

    def separate_from_other_enemies(self, grid):
        """
        Moves the enemy away from nearby enemies to avoid overlapping.

        Args:
            grid (dict): A grid containing positions of other enemies.
        """
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
        """
        Returns the tile position of the given pixel position.

        Args:
            position (tuple): The pixel position (x, y) to convert.

        Returns:
            tuple: The tile position (x, y).
        """
        return int(position[0] // self.tile_size), int(position[1] // self.tile_size)
