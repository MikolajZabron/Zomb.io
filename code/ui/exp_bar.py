from utilities.settings import *
from ui.user_interface import UserInterfaceElement
from player.player import Player


class ExperienceBar(UserInterfaceElement):
    def __init__(self, player: Player):
        super().__init__()
        self.player = player
        self.transition_speed = BAR_TRANSITION_SPEED
        self.screen = pygame.display.get_surface()
        self.exp_ratio = SCREEN_WIDTH / PLAYER_EXPERIENCE_NEED

    def update(self):
        if self.player.exp < self.player.target_exp:
            self.player.exp += self.transition_speed
        if self.player.exp > self.player.target_exp:
            self.player.exp -= self.transition_speed

        self.exp_ratio = (SCREEN_WIDTH - SCREEN_WIDTH / 8 - 225) / self.player.exp_need

    def draw(self):
        pygame.draw.rect(self.screen, (0, 255, 0), (SCREEN_WIDTH / 8 + 110,
                                                    SCREEN_HEIGHT - 100, self.player.exp * self.exp_ratio, 70))
