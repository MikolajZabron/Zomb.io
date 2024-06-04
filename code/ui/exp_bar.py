from utilities.settings import *
from ui.user_interface import UserInterfaceElement
from player.player import Player


class ExperienceBar(UserInterfaceElement):
    """
    Represents an experience bar in the game's user interface.

    Attributes:
        player (Player): The player object associated with the experience bar.
        transition_speed (int): The speed at which the experience bar transitions.
        screen (pygame.Surface): The surface representing the game screen.
        exp_ratio (float): The ratio of experience points to screen width.

    Methods:
        __init__(player): Constructor method for the ExperienceBar class.
        update(): Updates the experience bar.
        draw(): Draws the experience bar on the screen.
    """

    def __init__(self, player: Player):
        """
        Constructor method for the ExperienceBar class.

        Args:
            player (Player): The player object associated with the experience bar.
        """
        super().__init__()
        self.player = player
        self.transition_speed = EXP_BAR_TRANSITION_SPEED
        self.screen = pygame.display.get_surface()
        self.exp_ratio = SCREEN_WIDTH / PLAYER_EXPERIENCE_NEED

    def update(self):
        """
        Updates the experience bar.
        """
        if self.player.exp < self.player.target_exp:
            self.player.exp += self.transition_speed
        if self.player.exp > self.player.target_exp:
            self.player.exp -= self.transition_speed

        self.exp_ratio = (SCREEN_WIDTH - SCREEN_WIDTH / 8 - 225) / self.player.exp_need

    def draw(self):
        """
        Draws the experience bar on the screen.
        """
        pygame.draw.rect(self.screen, (0, 255, 0), (SCREEN_WIDTH / 8 + 110,
                                                    SCREEN_HEIGHT - 100, self.player.exp * self.exp_ratio, 70))
