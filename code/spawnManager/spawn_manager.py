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

    def spawn_start(self, groups: tuple):
        for j in range(10):
            random_x = randint(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
            random_y = randint(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
            enemy = RegularEnemy(groups, Vector2(random_x, random_y), 5, 10, 2)

    def spawn(self, groups: tuple, time):
        if self.wave_id > self.max_wave:
            return
        if time % 100 == 0:
            for i in range(self.spawn_data[self.wave_id][0]):
                random_x = randint(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
                random_y = randint(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
                enemy = RegularEnemy(groups, Vector2(random_x, random_y), 5, 10, 2)
            self.wave_id += 1
