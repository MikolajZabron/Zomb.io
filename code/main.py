import sys
from collections import defaultdict
from math import sqrt
import random

import pygame
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame
from structures.structure import Structure

from enemies.police_enemy import PoliceEnemy
from weapons.melee import Melee
from utilities.settings import *
from player.player import Player
from ui.health_bar import HealthBar
from ui.exp_bar import ExperienceBar
from weapons.bullet_template import BulletTemplate
from world import World
from utilities.camera_group import CameraGroup
from ui.ui_graphic import UIGraphic
from ui.skill_box import SkillBox
from structures.structure import Ground, CollisionBoundary
from spawnManager.spawn_manager import SpawnManager


class Zombio:
    """
    Main game class
    """

    def __init__(self):

        # Setup
        pygame.init()
        self.font = pygame.font.Font(None, 74)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # , pygame.FULLSCREEN
        pygame.display.set_caption('Zombio')
        self.clock = pygame.time.Clock()

        # Flags
        self.running = True
        self.freeze = False
        self.paused = False
        self.in_menu = True
        self.left = False
        self.mid = False
        self.right = False
        self.flag1 = True
        self.flag2 = True

        tmx_data = load_pygame("new_map/data/map/new_map.tmx")

        self.all_sprites = pygame.sprite.Group()
        self.ground = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.structures = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.skills = pygame.sprite.Group()
        self.enemy_attacks = pygame.sprite.Group()
        self.map_borders = pygame.sprite.Group()
        self.spawn_points = pygame.sprite.Group()

        # Objects initialization
        self.current_world = World()  # In future used class for now does nothing
        self.camera_group = CameraGroup(BACKGROUND_IMAGE, (self.ground, self.decorations, self.structures,
                                                           self.enemies, self.enemy_attacks, self.bullets, self.skills))
        self.player = Player((-100, 0), (self.all_sprites, self.camera_group), PLAYER_ANIMATION)
        self.spawn_range = CollisionBoundary((0, 0), 300, 300, ())
        self.health_bar = HealthBar(self.player)
        self.exp_bar = ExperienceBar(self.player)
        self.ui_graphic = UIGraphic((SCREEN_WIDTH/2 + 60, SCREEN_HEIGHT - 270))
        self.skill_boxes = []

        # Calculate map dimensions and offset
        map_width = tmx_data.width * tmx_data.tilewidth
        map_height = tmx_data.height * tmx_data.tileheight
        offset_x = map_width // 2
        offset_y = map_height // 2
        print("Offset", offset_x)
        print("Offset", offset_y)

        for layer in tmx_data.visible_layers:
            if layer.name == "ground" and isinstance(layer, TiledTileLayer):
                for x, y, surf in layer.tiles():
                    pos = ((x * tmx_data.tilewidth) - offset_x, (y * tmx_data.tileheight) - offset_y)
                    Ground(pos, surf, (self.all_sprites, self.camera_group, self.ground))
            if layer.name == "decorations" and isinstance(layer, TiledTileLayer):
                for x, y, surf in layer.tiles():
                    pos = ((x * tmx_data.tilewidth) - offset_x, (y * tmx_data.tileheight) - offset_y)
                    Ground(pos, surf, (self.all_sprites, self.camera_group, self.decorations))

        for obj in tmx_data.objects:
            pos = (obj.x - offset_x, obj.y - offset_y)
            if obj.name == "objects":
                Structure(pos, obj.image, (self.all_sprites, self.camera_group, self.structures))
            if obj.name == "wall":
                CollisionBoundary(pos, obj.width, obj.height,
                                  (self.all_sprites, self.camera_group, self.map_borders))
            if obj.name == "spawn":
                CollisionBoundary(pos, obj.width, obj.height,
                                  (self.camera_group, self.spawn_points))

        self.last_shot_time = 0
        self.selected_skill_index = 1
        self.skill_list = []

        self.selected_item = 0
        self.selected_menu_item = 0

        self.spawn_manager = SpawnManager(self.spawn_points)

        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.set_alpha(128)
        self.overlay.fill((0, 0, 0))

    def start(self) -> None:
        """
        Main game loop

        :return: None
        """

        while self.running:
            self.check_event()

            if self.in_menu:
                self.update_menu()
            if not self.in_menu:
                if not self.paused:
                    if not self.freeze:
                        self.current_world.start()
                        self.update_objects()
                        self.update_screen()
                    elif self.freeze:
                        self.freeze_update()
                        self.skill_pick()
                if self.paused:
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
                    self.paused = not self.paused
                if event.key == pygame.K_l:
                    self.player.gain_experience(10)
                if self.freeze:
                    if event.key == pygame.K_a:
                        for skill in self.skills:
                            skill.selected = False
                        self.selected_skill_index = (self.selected_skill_index - 1) % len(self.skill_list)
                        self.skills.sprites()[self.selected_skill_index].selected = True
                    elif event.key == pygame.K_d:
                        for skill in self.skills:
                            skill.selected = False
                        self.selected_skill_index = (self.selected_skill_index + 1) % len(self.skill_list)
                        self.skills.sprites()[self.selected_skill_index].selected = True
                    elif event.key == pygame.K_RETURN:
                        if self.selected_skill_index == 0:
                            self.left = True
                        if self.selected_skill_index == 1:
                            self.mid = True
                        elif self.selected_skill_index == 2:
                            self.right = True
                if self.paused:
                    if event.key == pygame.K_w:
                        self.selected_item = (self.selected_item - 1) % 2
                    elif event.key == pygame.K_s:
                        self.selected_item = (self.selected_item + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item == 0:
                            self.paused = False
                        elif self.selected_item == 1:
                            sys.exit()
                if self.in_menu:
                    if event.key == pygame.K_w:
                        self.selected_menu_item = (self.selected_menu_item - 1) % 2
                    elif event.key == pygame.K_s:
                        self.selected_menu_item = (self.selected_menu_item + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if self.selected_menu_item == 0:
                            self.in_menu = False
                        elif self.selected_menu_item == 1:
                            sys.exit()
                if self.player.end_game:
                    if event.key == pygame.K_w:
                        self.selected_item = (self.selected_item - 1) % 2
                    elif event.key == pygame.K_s:
                        self.selected_item = (self.selected_item + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if self.selected_item == 0:
                            self.in_menu = True
                        elif self.selected_item == 1:
                            sys.exit()

    def player_range_attack(self):
        current_time = pygame.time.get_ticks() / 1000
        time_since_last_shot = current_time - self.last_shot_time
        if time_since_last_shot >= 1 / self.player.attack_speed:
            bullet = BulletTemplate(self.player.rect.center, self.nearest_enemy()[0].rect.center,
                                    (self.all_sprites, self.bullets, self.camera_group))
            self.last_shot_time = current_time

    def player_melee_attack(self, whom):
        current_time = pygame.time.get_ticks() / 1000
        time_since_last_shot = current_time - self.last_shot_time
        if time_since_last_shot >= 1 / self.player.attack_speed:
            melee = Melee(self.player.rect.center, self.camera_group)
            self.last_shot_time = current_time
            if not melee.dealt_damage:
                whom.take_damage(self.player.damage, self.player)
            melee.deal_damage()

    def player_level_up(self):
        if self.player.target_exp >= self.player.exp_need:
            self.player.level_up()
            self.freeze = True
            self.skill_draw()

    def skill_draw(self):

        while self.flag1:
            self.skill_list = []
            while len(self.skill_list) < 3:
                skill = self.skill_lottery()
                if skill not in self.skill_list:
                    self.skill_list.append(skill)

            left = SkillBox((SCREEN_WIDTH / 2 - 300, -500), self.skill_list[0], False)
            self.skills.add(left)
            mid = SkillBox((SCREEN_WIDTH / 2, -700), self.skill_list[1], True)
            self.skills.add(mid)
            right = SkillBox((SCREEN_WIDTH / 2 + 300, -900), self.skill_list[2], False)
            self.skills.add(right)

            self.flag1 = False

        self.skill_pick()

    def skill_pick(self):
        if self.left:
            self.left = False
            self.skills.sprites()[0].selected = True
            self.player.skill_choice(self.skill_list[0])
            self.skills.empty()
            self.freeze = False
        if self.mid:
            self.mid = False
            self.skills.sprites()[1].selected = True
            self.player.skill_choice(self.skill_list[1])
            self.skills.empty()
            self.freeze = False
        if self.right:
            self.right = False
            self.skills.sprites()[2].selected = True
            self.player.skill_choice(self.skill_list[2])
            self.skills.empty()
            self.freeze = False

    def skill_lottery(self):
        i = random.randint(1, 3)
        if i == 1:
            return "adbuff"
        elif i == 2:
            return "new_weapon"
        elif i == 3:
            return "hp_max"

    def nearest_enemy(self):
        closest_enemy = None
        closest_distance = float('inf')

        for enemy in self.enemies:
            distance = sqrt(pow(enemy.rect.centerx - self.player.rect.centerx, 2)
                            + pow(enemy.rect.centery - self.player.rect.centery, 2))

            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy, closest_distance

    def update_grid(self):
        grid = defaultdict(list)
        for enemy in self.enemies:
            tile_pos = enemy.tile_position(enemy.rect.center)
            grid[tile_pos].append(enemy)
        return grid

    def collision(self):
        for bullet in self.bullets:
            bullet.collision(self.enemies, self.player.damage, self.player)
        for bullet in self.enemy_attacks:
            bullet.check_collision(self.player)

    def update_objects(self) -> None:  # Temporary different approach in future
        """
        Method responsible for updating the position of all
        :return: None

        """
        grid = self.update_grid()
        self.spawn_manager.check_timers((self.all_sprites, self.enemies, self.camera_group), self.spawn_range)
        self.collision()
        for enemy in self.enemies:
            if isinstance(enemy, PoliceEnemy):
                enemy.attack(pygame.Vector2(self.player.rect.center),
                             (self.all_sprites, self.enemy_attacks, self.camera_group))
            enemy.calculate_movement(pygame.Vector2(self.player.rect.x, self.player.rect.y))
            enemy.check_collision(self.player, self.structures)
            enemy.movement(structures=self.structures, borders=self.map_borders, grid=grid)
        if self.nearest_enemy()[0] and self.player.bullet_range > self.nearest_enemy()[1]:
            self.player_range_attack()
        if self.nearest_enemy()[0] and self.player.melee_range > self.nearest_enemy()[1]:
            self.player_melee_attack(self.nearest_enemy()[0])
        self.player_level_up()
        self.player.update(self.structures, self.map_borders)
        # Update anti spawn range to be at player position
        self.spawn_range.rect.center = self.player.rect.center
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
        self.ui_graphic.draw()
        if self.paused or self.player.end_game:
            self.screen.blit(self.overlay, (0, 0))

            paused_rect = PAUSED_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 300))
            exit_rect = EXIT_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 220))
            return_rect = RETURN_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120))

            if self.selected_item == 1:
                exit_rect = EXIT_WHITE_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 220))
                self.screen.blit(EXIT_WHITE_IMAGE, exit_rect.topleft)
                self.screen.blit(RETURN_IMAGE, return_rect.topleft)
            elif self.selected_item == 0:
                return_rect = RETURN_WHITE_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120))
                self.screen.blit(EXIT_IMAGE, exit_rect.topleft)
                self.screen.blit(RETURN_WHITE_IMAGE, return_rect.topleft)

            if not self.player.end_game:
                self.screen.blit(PAUSED_IMAGE, paused_rect.topleft)

        if self.player.end_game:
            game_over_text = self.font.render('GAME OVER', True, (0, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200))
            self.screen.blit(game_over_text, game_over_rect.topleft)

        pygame.display.update()
        self.clock.tick(60)

    def freeze_update(self):
        self.camera_group.custom_draw(self.player)
        for skill_box in self.skills.sprites():
            skill_box.draw()
        pygame.display.update()
        self.clock.tick(60)

    def update_menu(self):

        self.screen.blit(MENU_IMAGE, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

        zombio_rect = ZOMBIO_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 300))
        start_rect = START_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120))
        exit_rect = EXIT_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 220))

        if self.selected_menu_item == 1:
            exit_rect = EXIT_WHITE_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 220))
            self.screen.blit(EXIT_WHITE_IMAGE, exit_rect.topleft)
            self.screen.blit(START_IMAGE, start_rect.topleft)

        elif self.selected_menu_item == 0:
            start_rect = START_WHITE_IMAGE.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120))
            self.screen.blit(EXIT_IMAGE, exit_rect.topleft)
            self.screen.blit(START_WHITE_IMAGE, start_rect.topleft)

        self.screen.blit(ZOMBIO_IMAGE, zombio_rect.topleft)

        pygame.display.update()


if __name__ == '__main__':
    game = Zombio()
    game.start()
