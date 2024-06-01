from random import randint
from pygame.math import Vector2
from pytmx import TiledTileLayer

from structures.structure import Structure
from utilities.settings import SCREEN_WIDTH, SCREEN_HEIGHT
from enemies.normal_enemy import RegularEnemy


class SpawnManager:
    def __init__(self):
        self.spawn_data = [[10, "normal"], [10, "normal"]]
        self.wave_id = 0
        self.max_wave = 2
        self.initial_spawn_rate = 5000
        self.spawn_rate_decay = 500
        self.special_wave_chance = 0.2
        self.last_spawn_time = 0

    def spawn_start(self, groups: tuple):
        for j in range(10):
            random_x = randint(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
            random_y = randint(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
            enemy = RegularEnemy(groups, Vector2(random_x, random_y), 5, 10, 2)

    def spawn(self, groups: tuple, time):
        if current_time - self.last_spawn_time >= self.initial_spawn_rate:
            if self.current_wave < self.max_wave:
                self.current_wave += 1
                self.spawn_wave(groups)
                self.last_spawn_time = current_time
