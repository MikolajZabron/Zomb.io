from utilities.settings import *
from ui.user_interface import UserInterfaceElement


class SkillBox(UserInterfaceElement):
    """
    Represents a skill box in the game's user interface.

    Attributes:
        position (tuple): The position of the skill box.
        skill (str): The type of skill associated with the skill box.
        select (bool): Indicates whether the skill box is selected or not.
        image (pygame.Surface): The surface representing the skill box.
        screen (pygame.Surface): The surface representing the game screen.
        speed (int): The transition speed of the skill box.
        selected (bool): Indicates whether the skill box is selected or not.

    Methods:
        __init__(position, skill, select): Constructor method for the SkillBox class.
        update(): Updates the position of the skill box.
        draw(): Draws the skill box on the screen.
    """

    def __init__(self, position, skill, select):
        """
        Constructor method for the SkillBox class.

        Args:
            position (tuple): The position of the skill box.
            skill (str): The type of skill associated with the skill box.
            select (bool): Indicates whether the skill box is selected or not.
        """
        super().__init__()
        self.image = pygame.image.load(f"images/skill_{skill}.png").convert_alpha()
        self.screen = pygame.display.get_surface()
        self.position = position
        self.rect = self.image.get_rect(center=position)
        self.speed = SKILLBOX_TRANSITION_SPEED
        self.selected = select

        self.draw()

    def update(self):
        """
        Updates the position of the skill box.
        """
        if self.rect.y >= SCREEN_HEIGHT / 2 - 200:
            self.rect.y = SCREEN_HEIGHT / 2 - 200
            self.speed = 0
        else:
            self.rect.y += self.speed

    def draw(self):
        """
        Draws the skill box on the screen.
        """
        self.update()
        self.screen.blit(self.image, self.rect)
        if self.selected:
            border_color = (255, 255, 255)
            border_width = 2
            pygame.draw.rect(self.screen, border_color, self.rect, border_width)
