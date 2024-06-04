from enemies.police_enemy import PoliceEnemy
from utilities.settings import *
from enemies.normal_enemy import RegularEnemy
from enemies.riot_enemy import RiotEnemy
from random import randint
from pygame.math import Vector2


class Wave:
    """
    Represents a wave of enemies to be spawned in the game.

    Attributes:
        _enemy_types (list): List of enemy types in the wave.
        _spawn_rates (list): List of spawn rates for each enemy type.
        spawn_numbers (list): List of number of enemies to spawn for each enemy type.
        duration (float): Duration of the wave in seconds.
        spawn_times (list): List of times when enemies of each type were last spawned.
        mutation_statistic (int): Statistic for mutations in enemy waves.
        spawn_points (list): List of available spawn points for enemies.

    Methods:
        __init__(enemy_types, spawn_rates, spawn_numbers, duration): Constructor method for the Wave class.
        update(current_time, groups, spawn_points, spawn_range): Updates the wave and spawns enemies if necessary.
        spawn(num, enemy_type, groups): Spawns enemies of a specified type.
        check_spawn_availability(spawn_points, spawn_range): Checks available spawn points for enemies.
    """

    def __init__(self, enemy_types, spawn_rates, spawn_numbers, duration):
        """
        Constructor method for the Wave class.

        Args:
            enemy_types (list): List of enemy types in the wave.
            spawn_rates (list): List of spawn rates for each enemy type.
            spawn_numbers (list): List of number of enemies to spawn for each enemy type.
            duration (float): Duration of the wave in seconds.
        """
        self._enemy_types = enemy_types
        self._spawn_rates = spawn_rates
        self.spawn_numbers = spawn_numbers
        self.duration = duration
        self.spawn_times = [0.0 for _ in self._spawn_rates]
        self.mutation_statistic = 0
        self.spawn_points = []

    def update(self, current_time, groups, spawn_points, spawn_range):
        """
        Updates the wave and spawns enemies if necessary.

        Args:
            current_time (float): Current time in seconds.
            groups (pygame.sprite.AbstractGroup): Tuple of groups to which enemies belong.
            spawn_points (list): List of available spawn points for enemies.
            spawn_range (pygame.Rect): Range for enemy spawns.
        """
        for i in range(len(self.spawn_times)):
            if current_time - self.spawn_times[i] >= self._spawn_rates[i]:
                self.check_spawn_availability(spawn_points, spawn_range)
                self.spawn(self.spawn_numbers[i], self._enemy_types[i], groups)
                self.spawn_times[i] = current_time

    def spawn(self, num, enemy_type, groups: pygame.sprite.AbstractGroup):
        """
        Spawns enemies of a specified type.

        Args:
            num (int): Number of enemies to spawn.
            enemy_type (str): Type of enemy to spawn.
            groups (pygame.sprite.AbstractGroup): Tuple of groups to which enemies belong.
        """
        for i in range(num):
            random_spawn_point = randint(0, len(self.spawn_points) - 1)
            x, y = self.spawn_points[random_spawn_point].rect.center
            if enemy_type == "regular":
                RegularEnemy(groups, Vector2(x, y), REGULAR_ENEMY_SPEED,
                             REGULAR_ENEMY_HP + self.mutation_statistic, REGULAR_ENEMY_DAMAGE + self.mutation_statistic,
                             ENEMY_REGULAR_ANIMATION)
            elif enemy_type == "regular horde":
                for j in range(5):
                    if j % 2 == 0:
                        x += 32
                    else:
                        y += 32
                    RegularEnemy(groups, Vector2(x, y), REGULAR_ENEMY_SPEED,
                                 REGULAR_ENEMY_HP + self.mutation_statistic,
                                 REGULAR_ENEMY_DAMAGE + self.mutation_statistic,
                                 ENEMY_REGULAR_ANIMATION)
            elif enemy_type == "police":
                PoliceEnemy(groups, Vector2(x, y), POLICE_ENEMY_SPEED,
                            POLICE_ENEMY_HP + self.mutation_statistic, POLICE_ENEMY_DAMAGE + self.mutation_statistic,
                            ENEMY_POLICE_ANIMATION)
            elif enemy_type == "police horde":
                for j in range(4):
                    if j % 2 == 0:
                        x += 32
                    else:
                        y += 32
                    PoliceEnemy(groups, Vector2(x, y), POLICE_ENEMY_SPEED,
                                POLICE_ENEMY_HP + self.mutation_statistic,
                                POLICE_ENEMY_DAMAGE + self.mutation_statistic,
                                ENEMY_POLICE_ANIMATION)
            elif enemy_type == "riot":
                RiotEnemy(groups, Vector2(x, y), RIOT_ENEMY_SPEED,
                          RIOT_ENEMY_HP + self.mutation_statistic, RIOT_ENEMY_DMG + self.mutation_statistic,
                          ENEMY_RIOT_ANIMATION)

    def check_spawn_availability(self, spawn_points, spawn_range):
        """
        Checks available spawn points for enemies.

        Args:
            spawn_points (list): List of available spawn points for enemies.
            spawn_range (pygame.Rect): Range for enemy spawns.
        """
        available_spawn_points = []
        for spawn_point in spawn_points:
            if not pygame.sprite.collide_rect(spawn_range, spawn_point):
                available_spawn_points.append(spawn_point)
        self.spawn_points = available_spawn_points

