import pygame.sprite

from enemies.zombie_projectile import Projectile
from player.player import Player
from weapons.bullet_template import BulletTemplate


class CameraGroup(pygame.sprite.Group):
    """
    Custom sprite group that is made so that camera behaviour in proper way
    """

    def __init__(self, background_image):
        super().__init__()
        self.screen = pygame.display.get_surface()

        # Camera Offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2

        # Ground
        self.ground_surface = background_image.convert_alpha()
        self.ground_rect = self.ground_surface.get_rect(center=(0, 0))

    def center_target_camera(self, target) -> None:
        """
        Method for centering the camera with the specified target

        :param target: object that the camera will center on
        :return: None
        """

        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, target) -> None:
        """
        Method for custom drawing sprite in camera group

        :param target: object that the camera will center on
        :return: None
        """

        self.center_target_camera(target)

        # Ground
        # ground_offset = self.ground_rect.topleft - self.offset
        # self.screen.blit(self.ground_surface, ground_offset)

        # Objects
        non_bullet_sprites = []
        bullet_sprites = []

        for sprite in self.sprites():
            if isinstance(sprite, Projectile) or isinstance(sprite, BulletTemplate):
                bullet_sprites.append(sprite)
            else:
                non_bullet_sprites.append(sprite)

        # Draw non-bullet sprites first
        for sprite in sorted(non_bullet_sprites, key=lambda sprite: sprite.rect.bottom):
            offset_position = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_position)

        # Draw bullet sprites last
        for sprite in bullet_sprites:
            offset_position = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_position)

    def update(self, *args, **kwargs):
        # Update all sprites except player
        for sprite in self.sprites():
            if not isinstance(sprite, Player):
                sprite.update(*args, **kwargs)
