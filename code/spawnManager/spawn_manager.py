from random import randint, random
from spawnManager.wave import Wave
from utilities.settings import *


class SpawnManager:
    """
    Manages the spawning of enemy waves in the game.

    Attributes:
        spawn_points (list): List of spawn points for enemies.
        wave_number (int): The current wave number.
        time_since_last_wave (float): Time elapsed since the last wave.
        mutation_statistic (int): Statistic for mutations in enemy waves.
        current_wave (Wave): The current wave of enemies.

    Methods:
        __init__(spawn_points): Constructor method for the SpawnManager class.
        create_wave(): Creates a new wave of enemies.
        check_timers(groups, spawn_range): Checks timers to determine when to spawn a new wave.
    """

    def __init__(self, spawn_points):
        """
        Constructor method for the SpawnManager class.

        Args:
            spawn_points (list): List of spawn points for enemies.
        """
        # Wave Info
        self.spawn_points = spawn_points
        self.wave_number = 0
        self.time_since_last_wave = 0
        self.mutation_statistic = 0
        self.current_wave = Wave(**PREDEFINED_WAVES[0])

    def create_wave(self):
        """
        Creates a new wave of enemies.
        """
        mutation_random = random()
        is_mutated = mutation_random < MUTATION_CHANCE
        if is_mutated:
            self.mutation_statistic += MUTATION_HP_INCREASE
        if self.wave_number < len(PREDEFINED_WAVES):
            self.current_wave = Wave(**PREDEFINED_WAVES[self.wave_number])
        else:
            random_wave_config = randint(0, len(WAVE_TYPES) - 1)
            self.current_wave = Wave(**WAVE_TYPES[random_wave_config])
        self.current_wave.mutation_statistic = self.mutation_statistic

    def check_timers(self, groups, spawn_range):
        """
        Checks timers to determine when to spawn a new wave.

        Args:
            groups (pygame.sprite.AbstractGroup): The groups to which enemies belong.
            spawn_range (int): The spawn range for enemies.
        """
        current_time = pygame.time.get_ticks() / 1000  # Get current time in seconds
        if current_time - self.time_since_last_wave >= self.current_wave.duration:
            self.wave_number += 1
            self.create_wave()
            self.time_since_last_wave = current_time
        self.current_wave.update(current_time, groups, self.spawn_points, spawn_range)
