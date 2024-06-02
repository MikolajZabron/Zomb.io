from random import randint
from spawnManager.wave import Wave
from utilities.settings import *


class SpawnManager:
    def __init__(self):
        # Wave Info
        self.wave_number = 0
        self.time_since_last_wave = 0
        self.current_wave = Wave(**PREDEFINED_WAVES[0])

    def create_wave(self):
        if self.wave_number < len(PREDEFINED_WAVES):
            self.current_wave = Wave(**PREDEFINED_WAVES[self.wave_number])
        else:
            random_wave_config = randint(0, len(WAVE_TYPES) - 1)
            print(random_wave_config)
            self.current_wave = Wave(**WAVE_TYPES[random_wave_config])

    def check_timers(self, groups, ranged_group):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.time_since_last_wave >= self.current_wave.duration:
            self.wave_number += 1
            self.create_wave()
            self.time_since_last_wave = current_time
        self.current_wave.update(current_time, groups, ranged_group)
