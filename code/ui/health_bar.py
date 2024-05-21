from utilities.settings import *
from ui.user_interface import UserInterfaceElement
from player.player import Player


class HealthBar(UserInterfaceElement):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.transition_speed = BAR_TRANSITION_SPEED / 5
        self.screen = pygame.display.get_surface()

    def update(self):
        if self.player.health < self.player.target_health:
            self.player.health += self.transition_speed
        if self.player.health > self.player.target_health:
            self.player.health -= self.transition_speed

    def draw(self):

        """
        bar_size = 100
        max_health = self.player.health_max
        current_health = self.player.health

        health_height = (current_health / max_health) * bar_size

        pygame.draw.rect(self.screen, (255, 0, 0),
                         (120, 826,
                          120, 82))"""

        bar_width = 120
        bar_height = 84
        bar_x = 120
        bar_y = 826
        max_health = self.player.health_max
        current_health = self.player.health

        health_ratio = current_health / max_health
        filled_bar_height = health_ratio * bar_height

        pygame.draw.rect(self.screen, (32, 32, 32), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y + (bar_height - filled_bar_height), bar_width, filled_bar_height))
