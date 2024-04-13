import pygame.sprite


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
        ground_offset = self.ground_rect.topleft - self.offset
        self.screen.blit(self.ground_surface, ground_offset)

        # Objects
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_position)
