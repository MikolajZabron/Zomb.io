# Settings

import pygame
from os.path import join

# Display Size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1280
TILE_SIZE = 64
ANIMATION_SPEED = 6

# Player Settings
PLAYER_IMAGE = pygame.image.load(join('images', 'player_placeholder.png'))
PLAYER_SPEED = 2
PLAYER_ATTACK_SPEED = 1
PLAYER_DAMAGE = 5

# Background Settings
BACKGROUND_IMAGE = pygame.image.load(join('images', 'background_placeholder.png'))

# Template enemy settings
ENEMY_TEMPLATE_IMAGE = pygame.image.load(join('images', 'enemy_template.png'))
ENEMY_TEMPLATE_HEALTH = 10

# Bullet template settings
BULLET_TEMPLATE_IMAGE = pygame.image.load(join('images', 'bullet_template.png'))
BULLET_SPEED = 10
