# Settings

import pygame
from os.path import join

# Display Size
SCREEN_WIDTH = 1280  # 1920 1600
SCREEN_HEIGHT = 960  # 1280 900
TILE_SIZE = 64
ANIMATION_SPEED = 6

# Player Settings
PLAYER_IMAGE = pygame.image.load(join('images', 'character_new_version.png'))
PLAYER_ANIMATION = [pygame.image.load(join('images', 'main_character', f'character1wersja1chodzenie{i}.png'))
                    for i in range(9)]
PLAYER_EXPERIENCE = 0
PLAYER_EXPERIENCE_NEED = 100
PLAYER_LEVEL = 1
PLAYER_SPEED = 4
PLAYER_ATTACK_SPEED = 1
PLAYER_DAMAGE = 5
PLAYER_HEALTH = 50
PLAYER_MAX_HEALTH = 50
PLAYER_RANGED_DAMAGE = 0
PLAYER_MELEE_DAMAGE = 0
PLAYER_MELEE_RANGE = 100
PLAYER_BULLET_RANGE = 500

# Background Settings
BACKGROUND_IMAGE = pygame.image.load(join('images', 'background_placeholder.png'))

# Enemy Settings
REGULAR_ENEMY_DAMAGE = 1
REGULAR_ENEMY_HP = 10
REGULAR_ENEMY_SPEED = 3
POLICE_ENEMY_DAMAGE = 3
POLICE_ENEMY_HP = 5
POLICE_ENEMY_SPEED = 3
RIOT_ENEMY_DMG = 4
RIOT_ENEMY_HP = 15
RIOT_ENEMY_SPEED = 3

# Template enemy settings
ENEMY_TEMPLATE_IMAGE = pygame.image.load(join('images', 'zombie_new_version.png'))
ENEMY_REGULAR_ANIMATION = [pygame.image.load(join('images', 'basic_zombie', f'zombie1wersja1chodzenie{i}.png'))
                           for i in range(9)]
ENEMY_POLICE_ANIMATION = [pygame.image.load(join('images', 'police_zombie', f'zombie2wersjachodzenie{i}.png'))
                          for i in range(9)]
ENEMY_RIOT_ANIMATION = [pygame.image.load(join('images', 'riot_zombie', f'zombie1wersja1chodzenie{i}.png'))
                        for i in range(9)]
ENEMY_TANK_IMAGE = pygame.image.load(join('images', 'police_zombie', 'zombie2wersjachodzenie1.png'))
ENEMY_TEMPLATE_HEALTH = 10

# Bullet template settings
BULLET_TEMPLATE_IMAGE = pygame.image.load(join('images', 'bullet.png'))
BULLET_SPEED = 10

# Melee template settings
MELEE_TEMPLATE = pygame.image.load(join('images', 'example of a weapon and 2 types of swing/swing.png'))

# UI Bar's settings
BAR_TRANSITION_SPEED = 5
EXP_BAR_TRANSITION_SPEED = 0.5

# UI Skillbox settings
SKILLBOX_TRANSITION_SPEED = 10

# UI Graphic settings
UI_GRAPHIC = pygame.image.load(join('images', 'UIZombie.png'))

# Wave type Information Settings
WAVE_TYPES = [
    {"enemy_types": ["regular"], "spawn_rates": [3.0], "spawn_numbers": [2], "duration": 10.0},
    {"enemy_types": ["regular", "police"], "spawn_rates": [3.0, 3.0], "spawn_numbers": [2, 3], "duration": 10.0},
    {"enemy_types": ["regular horde"], "spawn_rates": [3.0], "spawn_numbers": [2], "duration": 10.0},
    {"enemy_types": ["police"], "spawn_rates": [3.0], "spawn_numbers": [2], "duration": 5.0},
    {"enemy_types": ["police horde"], "spawn_rates": [3.0], "spawn_numbers": [2], "duration": 10.0},
    {"enemy_types": ["regular", "riot"], "spawn_rates": [3.0, 3.0], "spawn_numbers": [2, 4], "duration": 10.0},
]

# Predefined waves configuration
PREDEFINED_WAVES = [
    {"enemy_types": ["regular"], "spawn_rates": [3.0], "spawn_numbers": [2], "duration": 10.0},
    {"enemy_types": ["regular"], "spawn_rates": [3.0], "spawn_numbers": [3], "duration": 10.0},
    {"enemy_types": ["regular"], "spawn_rates": [3.0], "spawn_numbers": [4], "duration": 10.0},
    {"enemy_types": ["police", "regular"], "spawn_rates": [3.0, 4.0], "spawn_numbers": [2, 2], "duration": 10.0}
]

# Zombie mutation
MUTATION_CHANCE = 0.1
MUTATION_HP_INCREASE = 10
MUTATION_DMG_INCREASE = 2

# Paused images
PAUSED_IMAGE = pygame.image.load(join('images', 'paused.png'))
EXIT_IMAGE = pygame.image.load(join('images', 'exit.png'))
RETURN_IMAGE = pygame.image.load(join('images', 'return.png'))
START_IMAGE = pygame.image.load(join('images', 'start.png'))

PAUSED_WHITE_IMAGE = pygame.image.load(join('images', 'paused_white.png'))
EXIT_WHITE_IMAGE = pygame.image.load(join('images', 'exit_white.png'))
RETURN_WHITE_IMAGE = pygame.image.load(join('images', 'return_white.png'))
START_WHITE_IMAGE = pygame.image.load(join('images', 'start_white.png'))

# Menu settings
MENU_IMAGE = pygame.image.load(join('images', 'menu_image.png'))
ZOMBIO_IMAGE = pygame.image.load(join('images', 'zombio.png'))
