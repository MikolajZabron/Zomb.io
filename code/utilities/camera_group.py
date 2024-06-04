import pygame.sprite

from enemies.zombie_projectile import Projectile
from player.player import Player
from weapons.bullet_template import BulletTemplate


class CameraGroup(pygame.sprite.Group):
    """
    Custom sprite group that is made so that camera behaviour in proper way
    """

    def __init__(self, background_image, priority_groups):
        super().__init__()
        self.screen = pygame.display.get_surface()

        # Camera Offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2

        # Ground
        self.ground_surface = background_image.convert_alpha()
        self.ground_rect = self.ground_surface.get_rect(center=(0, 0))

        self.priority_groups = priority_groups

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

        for group in self.priority_groups:
            for sprite in group:
                offset_position = sprite.rect.center - self.offset
                self.screen.blit(sprite.image, offset_position)

        offset_position = target.rect.center - self.offset
        self.screen.blit(target.image, offset_position)

    def update(self, *args, **kwargs):
        # Update all sprites except player
        for sprite in self.sprites():
            if not isinstance(sprite, Player):
                sprite.update(*args, **kwargs)
