from utilities.settings import *
from ui.user_interface import UserInterfaceElement


class UIGraphic(UserInterfaceElement):
    """
    Represents a graphic element in the game's user interface.

    Attributes:
        position (tuple): The position of the UI graphic.
        image (pygame.Surface): The surface representing the UI graphic.
        screen (pygame.Surface): The surface representing the game screen.

    Methods:
        __init__(position): Constructor method for the UIGraphic class.
        draw(): Draws the UI graphic on the screen.
    """

    def __init__(self, position):
        """
        Constructor method for the UIGraphic class.

        Args:
            position (tuple): The position of the UI graphic.
        """
        super().__init__()
        self.image = UI_GRAPHIC.convert_alpha()
        self.image = pygame.transform.scale(self.image, (2000, 1000))
        self.rect = self.image.get_rect(center=position)
        self.screen = pygame.display.get_surface()

    def draw(self):
        """
        Draws the UI graphic on the screen.
        """
        self.screen.blit(self.image, self.rect)
