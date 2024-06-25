from utilities.graphical_object import Object
import random
import pygame


class Particle(Object):
    def __init__(self, position, groups):
        """
        Initialize a particle object.

        :param position: Initial position of the particle (tuple of x, y coordinates)
        :param groups: Groups to which the particle should belong (pygame.sprite.Group)
        """
        super().__init__(groups)
        self.pos = position
        self.size = random.randint(2, 5)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)
        self.image = pygame.Surface((self.size, self.size))
        self.image.set_alpha(0)
        self.screen = pygame.display.get_surface()
        self.sand_colors = [
            (237, 201, 175),
            (210, 180, 140),
            (189, 157, 110),
            (240, 220, 130),
            (194, 178, 128)
        ]
        color_index = random.randint(0, len(self.sand_colors) - 1)
        self.image.fill(self.sand_colors[color_index])
        self.velocity = [random.uniform(-0.5, 0.5), random.uniform(-1, 0)]
        self.lifespan = random.randint(50, 300)
        self.initial_lifespan = self.lifespan
        self.gravity = 0.1
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        """
        Update the particle's position, transparency, and check for deletion based on lifespan.

        :return: None
        """
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        fade_factor = self.lifespan / self.initial_lifespan
        self.image.set_alpha(int(255 * fade_factor))
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.lifespan:
            self.kill()
