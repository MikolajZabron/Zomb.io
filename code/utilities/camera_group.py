import pygame.sprite
from player.player import Player


class CameraGroup(pygame.sprite.Group):
    """
    Custom sprite group that handles camera behavior.
    """

    def __init__(self, background_image, priority_groups):
        """
        Constructor method for CameraGroup.

        Args:
            background_image (pygame.Surface): Background image of the game.
            priority_groups (list): List of priority sprite groups.
        """
        super().__init__()
        self.screen = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.screen.get_size()[0] // 2
        self.half_h = self.screen.get_size()[1] // 2

        self.ground_surface = background_image.convert_alpha()
        self.ground_rect = self.ground_surface.get_rect(center=(0, 0))

        self.priority_groups = priority_groups

    def center_target_camera(self, target) -> None:
        """
        Center the camera with the specified target.

        Args:
            target: Object that the camera will center on.
        """
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, target) -> None:
        """
        Custom method for drawing sprites in the camera group.

        Args:
            target: Object that the camera will center on.
        """
        self.center_target_camera(target)

        for group in self.priority_groups:
            for sprite in group:
                offset_position = sprite.rect.center - self.offset
                self.screen.blit(sprite.image, offset_position)

        offset_position = target.rect.center - self.offset
        self.screen.blit(target.image, offset_position)

    def update(self, *args, **kwargs):
        """
        Update method for the CameraGroup.
        """
        for sprite in self.sprites():
            if not isinstance(sprite, Player):
                sprite.update(*args, **kwargs)
