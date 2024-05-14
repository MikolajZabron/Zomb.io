from utilities.settings import *
from ui.user_interface import UserInterfaceElement
from player.player import Player


class HealthBar(UserInterfaceElement):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.transition_speed = BAR_TRANSITION_SPEED
        self.screen = pygame.display.get_surface()

    def update(self):
        if self.player.health < self.player.target_health:
            self.player.health += self.transition_speed
        if self.player.health > self.player.target_health:
            self.player.health -= self.transition_speed

    def draw(self):
        # Constants
        bar_size = SCREEN_WIDTH / 8
        max_health = self.player.health_max
        current_health = self.player.health

        health_height = (current_health / max_health) * bar_size

        pygame.draw.rect(self.screen, (255, 0, 0),
                         (2, SCREEN_HEIGHT - bar_size - 2 + (bar_size - health_height),
                          bar_size, health_height))

