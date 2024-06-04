import pygame.sprite


class Object(pygame.sprite.Sprite):
    """
    Abstract class, base for all graphical objects in the game

    This class serves as the foundation for all graphical objects within the game. It is an abstract class,
    meaning it should not be instantiated directly, but rather subclassed by specific types of graphical objects.

    Methods:
        __init__(groups): Constructor method for the Object class.
    """
    def __init__(self, groups):
        """
        Initializes the Object with the specified groups.

        Parameters
        ----------
        groups : AbstractGroup[_SpriteSupportsGroup]
            A list of groups to which this sprite belongs.
        """
        super().__init__(groups)
