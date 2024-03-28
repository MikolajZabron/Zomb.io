import pygame
import sys

import settings
from player import Player


class Zombio:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.running = True

        self.player = Player(self)

    def start(self):
        while self.running:
            self.check_event()
            self.update_objects()
            self.update_screen()

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_event_keydown(event)
            elif event.type == pygame.KEYUP:
                self.check_event_keyup(event)

    def check_event_keyup(self, event):
        if event.key == pygame.K_s:
            self.player.moving_right = False
        elif event.key == pygame.K_a:
            self.player.moving_left = False
        elif event.key == pygame.K_w:
            self.player.moving_up = False
        elif event.key == pygame.K_d:
            self.player.moving_down = False

    def check_event_keydown(self, event):
        if event.key == pygame.K_d:
            self.player.moving_right = True
        elif event.key == pygame.K_a:
            self.player.moving_left = True
        elif event.key == pygame.K_w:
            self.player.moving_up = True
        elif event.key == pygame.K_s:
            self.player.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def update_objects(self):
        self.player.update()

    def update_screen(self):
        self.player.blit_player()
        pygame.display.flip()


if __name__ == '__main__':
    game = Zombio()
    game.start()
