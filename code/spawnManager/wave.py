from enemies.police_enemy import PoliceEnemy
from utilities.settings import *
from enemies.normal_enemy import RegularEnemy
from enemies.riot_enemy import RiotEnemy
from random import randint
from pygame.math import Vector2


class Wave:
    def __init__(self, enemy_types, spawn_rates, spawn_numbers, duration):
        self._enemy_types = enemy_types
        self._spawn_rates = spawn_rates
        self.spawn_numbers = spawn_numbers
        self.duration = duration
        self.spawn_times = [0.0 for _ in self._spawn_rates]

    def update(self, current_time, groups, ranged_group):
        for i in range(len(self.spawn_times)):
            if current_time - self.spawn_times[i] >= self._spawn_rates[i]:
                self.spawn(self.spawn_numbers[i], self._enemy_types[i], groups, ranged_group)
                self.spawn_times[i] = current_time

    def spawn(self, num, enemy_type, groups: tuple, ranged_group):
        for i in range(num):
            random_x = randint(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
            random_y = randint(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
            if enemy_type == "regular":
                RegularEnemy(groups, Vector2(random_x, random_y), 3, 10, 1,
                             ENEMY_REGULAR_ANIMATION)
            elif enemy_type == "regular horde":
                for j in range(5):
                    if j % 2 == 0:
                        random_x += 32
                    else:
                        random_y += 32
                    RegularEnemy(groups, Vector2(random_x, random_y), 3, 10, 1,
                                 ENEMY_REGULAR_ANIMATION)
            elif enemy_type == "police":
                PoliceEnemy(groups + (ranged_group, ), Vector2(random_x, random_y), 3, 10, 1,
                            ENEMY_POLICE_ANIMATION, image=ENEMY_TANK_IMAGE)
            elif enemy_type == "police horde":
                for j in range(4):
                    if j % 2 == 0:
                        random_x += 32
                    else:
                        random_y += 32
                    PoliceEnemy(groups + (ranged_group, ), Vector2(random_x, random_y), 3, 10,
                                1, ENEMY_POLICE_ANIMATION)
            elif enemy_type == "riot":
                RiotEnemy(groups, Vector2(random_x, random_y), 3, 10, 1, ENEMY_RIOT_ANIMATION)
