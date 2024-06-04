from utilities.settings import *
from ui.user_interface import UserInterfaceElement


class SkillBox(UserInterfaceElement):
    def __init__(self, position, skill, select):
        super().__init__()
        self.image = pygame.image.load(f"images/skill_{skill}.png").convert_alpha()
        self.screen = pygame.display.get_surface()
        self.position = position
        self.rect = self.image.get_rect(center=position)
        self.speed = SKILLBOX_TRANSITION_SPEED
        self.selected = select

        self.draw()

    def update(self):
        if self.rect.y >= SCREEN_HEIGHT / 2 - 200:
            self.rect.y = SCREEN_HEIGHT / 2 - 200
            self.speed = 0
        else:
            self.rect.y += self.speed

    def draw(self):
        self.update()
        self.screen.blit(self.image, self.rect)
        if self.selected:
            border_color = (255, 255, 255)
            border_width = 2
            pygame.draw.rect(self.screen, border_color, self.rect, border_width)
