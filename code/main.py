import sys
from collections import defaultdict
from math import sqrt
import random

import pygame
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

from player.player_particles import Particle
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
    Main game class that initializes and manages the game.
    """

    def __init__(self):

        # Setup
        pygame.init()
        pygame.mixer.init()
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

        pygame.mixer.set_num_channels(3)
        tmx_data = load_pygame("new_map/data/map/new_map.tmx")
        self.main_song = pygame.mixer.Sound('images/Sounds/short-game-music-loop-38898.mp3')
        self.slash = pygame.mixer.Sound('images/Sounds/axe-slash-1-106748.mp3')
        self.skill_pick_sound = pygame.mixer.Sound('images/Sounds/collect-points-190037.mp3')
        self.start_game = pygame.mixer.Sound('images/Sounds/game-start-6104.mp3')
        self.game_over_sound = pygame.mixer.Sound('images/Sounds/game-over-arcade-6435.mp3')
        self.menu_song = pygame.mixer.Sound('images/Sounds/crime-sound-loop-28873.mp3')
        self.knife = pygame.mixer.Sound('images/Sounds/sword-sound-2-36274.mp3')
        self.shot = pygame.mixer.Sound('images/Sounds/086409_retro-gun-shot-81545.mp3')

        self.song_channel = pygame.mixer.Channel(0)
        self.sound_player_channel = pygame.mixer.Channel(1)
        self.sound_ui_channel = pygame.mixer.Channel(2)

        self.main_song.set_volume(0.5)
        self.shot.set_volume(0.3)

        self.sound_player_channel.set_volume(0.2)
        self.sound_ui_channel.set_volume(0.5)
        self.song_channel.set_volume(0.4)

        self.all_sprites = pygame.sprite.Group()
        self.ground = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.structures = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.skills = pygame.sprite.Group()
        self.player_attacks = pygame.sprite.Group()
        self.enemy_attacks = pygame.sprite.Group()
        self.map_borders = pygame.sprite.Group()
        self.spawn_points = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        self.current_world = World()
        self.camera_group = CameraGroup(BACKGROUND_IMAGE, (self.ground, self.decorations, self.structures,
                                                           self.particles, self.enemies, self.enemy_attacks, self.bullets, self.skills,
                                                           self.player_attacks))
        self.player = Player((-100, 0), (self.all_sprites, self.camera_group), PLAYER_ANIMATION)
        self.spawn_range = CollisionBoundary((0, 0), 300, 300, ())
        self.health_bar = HealthBar(self.player)
        self.exp_bar = ExperienceBar(self.player)
        self.ui_graphic = UIGraphic((SCREEN_WIDTH/2 + 60, SCREEN_HEIGHT - 270))
        self.skill_boxes = []
        self.skills = pygame.sprite.Group()


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
        self.last_hit_time = 0
        self.selected_skill_index = 1
        self.skill_list = []

        self.selected_item = 0
        self.selected_menu_item = 0

        self.spawn_manager = SpawnManager(self.spawn_points)

        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.set_alpha(128)
        self.overlay.fill((0, 0, 0))

        self.song_channel.play(self.menu_song, loops=-1)

    def start(self) -> None:
        """
        Main game loop. Controls the flow of the game, updating objects and managing different game states.

        :return: None
        """

        while self.running:
            self.check_event()

            if self.in_menu:
                self.update_menu()
            if not self.in_menu:
                if not self.paused:
                    if not self.player.end_game:
                        if not self.freeze:
                            self.current_world.start()
                            self.update_objects()
                            self.update_screen()
                        elif self.freeze:
                            self.update_screen()
                            self.skill_pick()
                if self.paused or self.player.end_game:
                    self.update_screen()

    def check_event(self) -> None:
        """
        Method that handles pygame events such as key presses, controlling game state transitions and actions.

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
                        self.sound_ui_channel.play(self.slash)
                        for skill in self.skills:
                            skill.selected = False
                        self.selected_skill_index = (self.selected_skill_index - 1) % len(self.skill_list)
                        self.skills.sprites()[self.selected_skill_index].selected = True
                    elif event.key == pygame.K_d:
                        self.sound_ui_channel.play(self.slash)
                        for skill in self.skills:
                            skill.selected = False
                        self.selected_skill_index = (self.selected_skill_index + 1) % len(self.skill_list)
                        self.skills.sprites()[self.selected_skill_index].selected = True
                    elif event.key == pygame.K_RETURN:
                        self.sound_ui_channel.play(self.skill_pick_sound)
                        if self.selected_skill_index == 0:
                            self.left = True
                        if self.selected_skill_index == 1:
                            self.mid = True
                        elif self.selected_skill_index == 2:
                            self.right = True
                if self.paused:
                    if event.key == pygame.K_w:
                        self.sound_ui_channel.play(self.slash)
                        self.selected_item = (self.selected_item - 1) % 2
                    elif event.key == pygame.K_s:
                        self.sound_ui_channel.play(self.slash)
                        self.selected_item = (self.selected_item + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        self.sound_ui_channel.play(self.skill_pick_sound)
                        if self.selected_item == 0:
                            self.paused = False
                        elif self.selected_item == 1:
                            sys.exit()
                if self.in_menu:
                    if event.key == pygame.K_w:
                        self.sound_ui_channel.play(self.slash)
                        self.selected_menu_item = (self.selected_menu_item - 1) % 2
                    elif event.key == pygame.K_s:
                        self.sound_ui_channel.play(self.slash)
                        self.selected_menu_item = (self.selected_menu_item + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if self.selected_menu_item == 0:
                            self.in_menu = False
                            self.sound_ui_channel.play(self.start_game)
                            self.song_channel.play(self.main_song, loops=-1)
                        elif self.selected_menu_item == 1:
                            sys.exit()
                if self.player.end_game:
                    if event.key == pygame.K_w:
                        self.sound_ui_channel.play(self.slash)
                        self.selected_item = (self.selected_item - 1) % 2
                    elif event.key == pygame.K_s:
                        self.sound_ui_channel.play(self.slash)
                        self.selected_item = (self.selected_item + 1) % 2
                    elif event.key == pygame.K_RETURN:
                        self.sound_ui_channel.play(self.skill_pick_sound)
                        if self.selected_item == 0:
                            self.in_menu = True
                        elif self.selected_item == 1:
                            sys.exit()

    def player_range_attack(self):
        """
        Method to execute the player's ranged attack.

        :return: None
        """
        current_time = pygame.time.get_ticks() / 1000
        time_since_last_shot = current_time - self.last_shot_time
        if time_since_last_shot >= 1 / self.player.attack_speed / self.player.ranged_weapons:
            bullet = BulletTemplate(self.player.rect.center, self.nearest_enemy()[0].rect.center,
                                    (self.all_sprites, self.bullets, self.camera_group))
            self.last_shot_time = current_time
            self.sound_player_channel.play(self.shot)

    def player_melee_attack(self, whom):
        """
        Method to execute the player's melee attack against a specific enemy.

        :param whom: The enemy to attack
        :return: None
        """
        current_time = pygame.time.get_ticks() / 1000
        time_since_last_hit = current_time - self.last_hit_time
        if time_since_last_hit >= 1 / self.player.attack_speed / self.player.melee_weapons:
            melee = Melee(self.player, whom, (self.camera_group, self.player_attacks))
            self.last_hit_time = current_time
            if not melee.dealt_damage:
                whom.take_damage(self.player.damage + self.player.melee_damage, self.player)
            melee.deal_damage()
            self.sound_player_channel.play(self.knife)

    def player_level_up(self):
        """
        Method to handle player level up logic.

        :return: None
        """
        if self.player.target_exp >= self.player.exp_need:
            self.player.level_up()
            self.freeze = True
            self.skill_draw()

    def skill_draw(self):
        """
        Method to draw and select skills for the player.

        :return: None
        """
        if self.flag1:
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
        """
        Method to handle player's skill selection.

        :return: None
        """
        if self.left:
            self.left = False
            self.skills.sprites()[0].selected = True
            self.player.skill_choice(self.skill_list[0])
            self.skills.empty()
            self.freeze = False
            self.selected_skill_index = 0
            self.flag1 = True
        if self.mid:
            self.mid = False
            self.skills.sprites()[1].selected = True
            self.player.skill_choice(self.skill_list[1])
            self.skills.empty()
            self.freeze = False
            self.selected_skill_index = 0
            self.flag1 = True
        if self.right:
            self.right = False
            self.skills.sprites()[2].selected = True
            self.player.skill_choice(self.skill_list[2])
            self.skills.empty()
            self.freeze = False
            self.selected_skill_index = 0
            self.flag1 = True

    def skill_lottery(self):
        """
        Method to randomly select a skill.

        :return: A string representing the chosen skill
        """
        i = random.randint(1, 9)
        if i == 1:
            return "ranged_weapon"
        elif i == 2:
            return "melee_weapon"
        elif i == 3:
            return "hp_max"
        elif i == 4:
            return "hp_res"
        elif i == 5:
            return "melee_dmg"
        elif i == 6:
            return "range_dmg"
        elif i == 7:
            return "range"
        elif i == 8:
            return "speed"
        elif i == 9:
            return "atk_speed"

    def nearest_enemy(self):
        """
        Method to find the nearest enemy to the player.

        :return: Tuple containing the closest enemy object and its distance
        """
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
        """
        Method updates enemies position on map grid

        :return: None

        """
        grid = defaultdict(list)
        for enemy in self.enemies:
            tile_pos = enemy.tile_position(enemy.rect.center)
            grid[tile_pos].append(enemy)
        return grid

    def collision(self):
        """
        Method responsible for checking selected collisions.

        :return: None

        """
        for bullet in self.bullets:
            bullet.collision(self.enemies, self.player.damage, self.player)
        for bullet in self.enemy_attacks:
            bullet.check_collision(self.player)

    def make_particles(self):
        if len(self.particles) < 30 and not self.player.not_moving:
            for i in range(5):
                Particle((self.player.rect.x + 16, self.player.rect.y + 50), self.particles)

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
        if self.player.ranged_weapons != 0:
            if self.nearest_enemy()[0] and self.player.bullet_range > self.nearest_enemy()[1]:
                self.player_range_attack()
        if self.player.melee_weapons != 0:
            if self.nearest_enemy()[0] and self.player.melee_range > self.nearest_enemy()[1]:
                self.player_melee_attack(self.nearest_enemy()[0])
        self.player_level_up()
        self.player.update(self.structures, self.map_borders)
        self.spawn_range.rect.center = self.player.rect.center
        self.health_bar.update()
        self.exp_bar.update()
        self.make_particles()
        for particle in self.particles:
            particle.update()

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
            self.sound_ui_channel.play(self.game_over_sound)
            game_over_text = self.font.render('GAME OVER', True, (0, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 200))

            game_over_score = self.font.render(f'SCORE : {self.player.whole_exp}', True, (0, 0, 0))
            game_over_rect2 = game_over_score.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
            self.screen.blit(game_over_text, game_over_rect.topleft)
            self.screen.blit(game_over_score, game_over_rect2.topleft)

        if self.freeze:
            for skill_box in self.skills.sprites():
                skill_box.draw()

        pygame.display.update()
        self.clock.tick(60)

    def update_menu(self):
        """
        Method responsible for updating menu.

        :return: None
        """

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
