import sys
from random import randint


from settings import *
from graphical_object import Object
from player import Player
from world import World
from camera_group import CameraGroup


class Tree(Object):
    """Temporary class made for camera testing purposes"""

    def __init__(self, position, group):
        super().__init__(group)

        # Setup
        self.image = pygame.image.load("images/tree_placeholder.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=position)


class Zombio:
    """
    Main game class
    """

    def __init__(self):

        # Setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # , pygame.FULLSCREEN
        pygame.display.set_caption('Zombio')
        self.clock = pygame.time.Clock()

        # Flags
        self.running = True

        # Objects initialization
        self.current_world = World()  # In future used class for now does nothing
        self.camera_group = CameraGroup(BACKGROUND_IMAGE)
        self.player = Player((0, 0), self.camera_group)

        # Temporary Trees Drawing
        for i in range(50):
            random_x = randint(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
            random_y = randint(-SCREEN_HEIGHT // 2, SCREEN_HEIGHT // 2)
            Tree((random_x, random_y), self.camera_group)

    def start(self) -> None:
        """
        Main game loop

        :return: None
        """

        while self.running:
            self.check_event()
            self.current_world.start()
            self.update_objects()
            self.update_screen()

    def check_event(self) -> None:
        """
        Method checking events such as pressed keys

        :return: None
        """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

    def update_objects(self) -> None:  # Temporary different approach in future
        """
        Method responsible for updating the position of all objects

        :return: None
        """

        self.player.update()

    def update_screen(self) -> None:
        """
        Method responsible for updating the screen of the game

        :return: None
        """

        self.player.blit_player()
        self.camera_group.update()
        self.camera_group.custom_draw(self.player)
        pygame.display.update()
        self.clock.tick(60)


if __name__ == '__main__':
    game = Zombio()
    game.start()
