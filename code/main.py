import sys
from math import sqrt
import random

import pygame
from pytmx import TiledTileLayer

from enemies.police_enemy import PoliceEnemy
from weapons.melee import Melee
from utilities.settings import *
from player.player import Player
from ui.health_bar import HealthBar
from ui.exp_bar import ExperienceBar
from weapons.bullet_template import BulletTemplate
from world import World
from utilities.camera_group import CameraGroup
from enemies.normal_enemy import RegularEnemy
from ui.ui_graphic import UIGraphic
from ui.skill_box import SkillBox
from structures.structure import Ground, CollisionBoundary
from spawnManager.spawn_manager import SpawnManager



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
        self.freeze = False
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

        # Objects initialization
        self.current_world = World()  # In future used class for now does nothing
        self.camera_group = CameraGroup(BACKGROUND_IMAGE, (self.ground, self.decorations, self.structures,
                                                           self.enemies, self.enemy_attacks, self.bullets, self.skills))
        self.player = Player((-100, 0), (self.all_sprites, self.camera_group), PLAYER_ANIMATION)
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
        self.last_shot_time = 0
        self.selected_skill_index = 1
        self.skill_list = []

        self.spawn_manager = SpawnManager()

    def start(self) -> None:
        """
        Main game loop

        :return: None
        """

        while self.running:
            self.check_event()
            if not self.freeze:
                self.current_world.start()
                self.update_objects()
                self.update_screen()
            elif self.freeze:
                self.freeze_update()
                self.skill_pick()

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

    def player_range_attack(self):  # Temporary
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
        self.spawn_manager.check_timers((self.all_sprites, self.enemies, self.camera_group))
        self.collision()
        for enemy in self.enemies:
            if isinstance(enemy, PoliceEnemy):
                enemy.attack(pygame.Vector2(self.player.rect.center),
                             (self.all_sprites, self.enemy_attacks, self.camera_group))
            enemy.calculate_movement(pygame.Vector2(self.player.rect.x, self.player.rect.y))
            enemy.check_collision(self.player, self.structures)
            enemy.movement(structures=self.structures, borders=self.map_borders)
        #if self.nearest_enemy()[0] and self.player.bullet_range > self.nearest_enemy()[1]:
        #    self.player_range_attack()
        if self.nearest_enemy()[0] and self.player.melee_range > self.nearest_enemy()[1]:
            self.player_melee_attack(self.nearest_enemy()[0])
        self.player_level_up()
        self.player.update(self.structures, self.map_borders)
        self.health_bar.update()
        self.exp_bar.update()
        print(len(self.enemies))

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

        pygame.display.update()
        self.clock.tick(60)

    def freeze_update(self):
        self.camera_group.custom_draw(self.player)
        for skill_box in self.skills.sprites():
            skill_box.draw()
        pygame.display.update()
        self.clock.tick(60)


if __name__ == '__main__':
    game = Zombio()
    game.start()
