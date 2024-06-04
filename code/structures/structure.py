from utilities.graphical_object import Object
import pygame


class Structure(Object):
    """
    Represents a structure in the game.

    Attributes:
        position (tuple): The position of the structure.
        surf (pygame.Surface): The surface representing the structure.
        groups (tuple): Tuple of groups to which the structure belongs.

    Methods:
        __init__(position, surf, groups): Constructor method for the Structure class.
    """

    def __init__(self, position, surf, groups):
        """
        Constructor method for the Structure class.

        Args:
            position (tuple): The position of the structure.
            surf (pygame.Surface): The surface representing the structure.
            groups (tuple): Tuple of groups to which the structure belongs.
        """
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=position)
        self.mask = pygame.mask.from_surface(self.image)


class CollisionBoundary(Object):
    """
    Represents a collision boundary in the game.

    Attributes:
        pos (tuple): The position of the collision boundary.
        width (int): The width of the collision boundary.
        height (int): The height of the collision boundary.
        groups (tuple): Tuple of groups to which the collision boundary belongs.

    Methods:
        __init__(pos, width, height, groups): Constructor method for the CollisionBoundary class.
    """

    def __init__(self, pos, width, height, groups):
        """
        Constructor method for the CollisionBoundary class.

        Args:
            pos (tuple): The position of the collision boundary.
            width (int): The width of the collision boundary.
            height (int): The height of the collision boundary.
            groups (tuple): Tuple of groups to which the collision boundary belongs.
        """
        super().__init__(groups)
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.image = pygame.Surface((width, height))
        self.image.set_alpha(0)


class Ground(Object):
    """
    Represents the ground in the game.

    Attributes:
        position (tuple): The position of the ground.
        surf (pygame.Surface): The surface representing the ground.
        groups (tuple): Tuple of groups to which the ground belongs.

    Methods:
        __init__(position, surf, groups): Constructor method for the Ground class.
    """

    def __init__(self, position, surf, groups):
        """
        Constructor method for the Ground class.

        Args:
            position (tuple): The position of the ground.
            surf (pygame.Surface): The surface representing the ground.
            groups (tuple): Tuple of groups to which the ground belongs.
        """
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=position)
