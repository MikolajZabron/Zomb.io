from utilities.settings import *
from ui.user_interface import UserInterfaceElement


class UIGraphic(UserInterfaceElement):
    def __init__(self, position):
        super().__init__()
        self.image = UI_GRAPHIC.convert_alpha()
        self.image = pygame.transform.scale(self.image, (2000, 1000))
        self.rect = self.image.get_rect(center=position)
        self.screen = pygame.display.get_surface()

    def draw(self):
        self.screen.blit(self.image, self.rect)
