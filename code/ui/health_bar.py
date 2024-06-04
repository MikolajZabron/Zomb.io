from utilities.settings import *
from ui.user_interface import UserInterfaceElement
from player.player import Player


class HealthBar(UserInterfaceElement):
    """
    Represents a health bar element in the game's user interface.

    Attributes:
        player (Player): The player object associated with the health bar.
        transition_speed (float): The transition speed of the health bar.
        screen (pygame.Surface): The surface representing the game screen.

    Methods:
        __init__(player): Constructor method for the HealthBar class.
        update(): Updates the health bar.
        draw(): Draws the health bar on the screen.
    """

    def __init__(self, player: Player):
        """
        Constructor method for the HealthBar class.

        Args:
            player (Player): The player object associated with the health bar.
        """
        super().__init__()
        self.player = player
        self.transition_speed = BAR_TRANSITION_SPEED / 5
        self.screen = pygame.display.get_surface()

    def update(self):
        """
        Updates the health bar.
        """
        if self.player.health < self.player.target_health:
            self.player.health += self.transition_speed
        if self.player.health > self.player.target_health:
            self.player.health -= self.transition_speed

    def draw(self):
        """
        Draws the health bar on the screen.
        """
        bar_width = 120
        bar_height = 84
        bar_x = 120
        bar_y = 826

        max_health = self.player.health_max
        current_health = self.player.health
        health_ratio = current_health / max_health
        filled_bar_height = health_ratio * bar_height

        pygame.draw.rect(self.screen, (32, 32, 32), (bar_x, bar_y, bar_width, bar_height))

        pygame.draw.rect(self.screen, (255, 0, 0),
                         (bar_x, bar_y + (bar_height - filled_bar_height), bar_width, filled_bar_height))
