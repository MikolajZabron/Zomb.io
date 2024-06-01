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
PLAYER_ENGINEER_DAMAGE = 0
PLAYER_MELEE_RANGE = 100
PLAYER_BULLET_RANGE = 500

# Background Settings
BACKGROUND_IMAGE = pygame.image.load(join('images', 'background_placeholder.png'))

# Template enemy settings
ENEMY_TEMPLATE_IMAGE = pygame.image.load(join('images', 'zombie_new_version.png'))
ENEMY_TEMPLATE_HEALTH = 10

# Bullet template settings
BULLET_TEMPLATE_IMAGE = pygame.image.load(join('images', 'bullet_template.png'))
BULLET_SPEED = 10

# Melee template settings
MELEE_TEMPLATE = pygame.image.load(join('images', 'example of a weapon and 2 types of swing/swing.png'))

# UI Bar's settings
BAR_TRANSITION_SPEED = 0.5

# UI Skillbox settings
SKILLBOX_TRANSITION_SPEED = 10

# UI Graphic settings
UI_GRAPHIC = pygame.image.load(join('images', 'UIZombie.png'))
