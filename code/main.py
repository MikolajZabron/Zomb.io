import sys
from math import sqrt
from random import randint

import pygame
from pytmx import TiledTileLayer

from utilities.settings import *
from player.player import Player
from ui.health_bar import HealthBar
from ui.exp_bar import ExperienceBar
from weapons.bullet_template import BulletTemplate
from world import World
from utilities.camera_group import CameraGroup
from enemies.normal_enemy import RegularEnemy
from weapons import bullet_template
from pytmx.util_pygame import load_pygame
from structures.structure import Structure




class Zombio:
    """
    Main game class
    """

    def __init__(self):

        # Setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # , pygame.FULLSCREEN
        pygame.display.set_caption('Zombio')
        self.clock = pygame.time.Clock()

        # Flags
        self.running = True

        tmx_data = load_pygame("Map/data/mapa/map.tmx")

        self.all_sprites = pygame.sprite.Group()
        self.structures = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.colliders = pygame.sprite.Group()
        self.ground = pygame.sprite.Group()


        # Objects initialization
        self.current_world = World()  # In future used class for now does nothing
        self.camera_group = CameraGroup(BACKGROUND_IMAGE)
        self.player = Player((0, 0), (self.all_sprites, self.camera_group))
        self.health_bar = HealthBar(self.player)
        self.exp_bar = ExperienceBar(self.player)

        for layer in tmx_data.visible_layers:
            if layer.name == "Structures" and isinstance(layer, TiledTileLayer):
                for x, y, surf in layer.tiles():
                    pos = (x * tmx_data.tilewidth, y * tmx_data.tileheight)
                    Structure(pos, surf, (self.camera_group, self.structures))

        self.last_shot_time = 0

        for j in range(5):
            random_x = randint(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
            random_y = randint(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
            enemy = RegularEnemy((self.all_sprites, self.enemies, self.camera_group),
                                 pygame.Vector2(random_x, random_y),
                                 3, 10, 2)

    def start(self) -> None:
        """
        Main game loop

        :return: None
        """

        while self.running:
            self.check_event()
            self.current_world.start()
            self.update_objects()
            self.update_screen()

    def check_event(self) -> None:
        """
        Method checking events such as pressed keys

        :return: None
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_ESCAPE:
                    self.player.take_damage(1)
                if event.key == pygame.K_l:
                    self.player.gain_experience(1)

    def player_attack(self):  # Temporary
        current_time = pygame.time.get_ticks() / 1000
        time_since_last_shot = current_time - self.last_shot_time
        if time_since_last_shot >= 1 / self.player.attack_speed:
            bullet = BulletTemplate(self.player.rect.center, self.nearest_enemy().rect.center,
                                    (self.all_sprites, self.bullets, self.camera_group))
            self.last_shot_time = current_time

    def nearest_enemy(self):
        closest_enemy = None
        closest_distance = float('inf')

        for enemy in self.enemies:
            distance = sqrt(pow(enemy.rect.centerx - self.player.rect.centerx, 2)
                            + pow(enemy.rect.centery - self.player.rect.centery, 2))

            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def collision(self):
        for bullet in self.bullets:
            bullet.collision(self.enemies, self.player.damage)

    def update_objects(self) -> None:  # Temporary different approach in future
        """
        Method responsible for updating the position of all
        :return: None

        """
        self.collision()
        for enemy in self.enemies:
            enemy.calculate_movement(pygame.Vector2(self.player.rect.x, self.player.rect.y))
            enemy.check_collision(self.player, self.structures)
            enemy.movement()
        if self.nearest_enemy():
            self.player_attack()
        self.player.update()
        self.player.check_collision(self.structures)
        self.health_bar.update()
        self.exp_bar.update()

    def update_screen(self) -> None:
        """
        Method responsible for updating the screen of the game

        :return: None
        """

        self.camera_group.update()
        self.camera_group.custom_draw(self.player)
        self.health_bar.draw()
        self.exp_bar.draw()
        pygame.display.update()
        self.clock.tick(60)


if __name__ == '__main__':
    game = Zombio()
    game.start()
