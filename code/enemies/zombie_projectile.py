import pygame

from player.player import Player
from utilities.graphical_object import Object
from utilities.settings import BULLET_TEMPLATE_IMAGE


class Projectile(Object):
    """
    A class to represent a projectile in the game.

    Inherits from the Object class.

    Attributes
    ----------
    direction : pygame.math.Vector2
        The direction of the projectile's movement.
    speed : float
        The speed of the projectile.
    damage : int
        The damage the projectile will inflict on collision.
    image : pygame.Surface
        The image of the projectile.
    rect : pygame.Rect
        The rectangular area of the image.
    screen : pygame.Surface
        The display surface for rendering the projectile.
    creation_time : int
        The time the projectile was created (in milliseconds).
    lifespan : int
        The lifespan of the projectile (in milliseconds).
    mask : pygame.mask.Mask
        The mask for collision detection.

    Methods
    -------
    update():
        Updates the projectile's position and checks if its lifespan is over.
    check_collision(player):
        Checks for collision with a player and inflicts damage.
    draw():
        Draws the projectile on the screen.
    """
    def __init__(self, position, direction, speed, damage, groups):
        """
        Constructs all the necessary attributes for the projectile object.

        Parameters
        ----------
        position : tuple
            The initial position of the projectile.
        direction : pygame.math.Vector2
            The direction of the projectile's movement.
        speed : float
            The speed of the projectile.
        damage : int
            The damage the projectile will inflict on collision.
        groups : list
            The groups to which this sprite belongs.
        """
        super().__init__(groups)
        self.image = BULLET_TEMPLATE_IMAGE.convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=position)
        self.direction = direction.normalize()
        self.speed = speed
        self.damage = damage
        self.screen = pygame.display.get_surface()
        self.creation_time = pygame.time.get_ticks()
        self.lifespan = 4000
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """
        Updates the projectile's position and checks if its lifespan is over.

        If the projectile's lifespan is exceeded, it is removed from all groups.
        """
        self.rect.move_ip(self.direction * self.speed)
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time > self.lifespan:
            self.kill()

    def check_collision(self, player: Player):
        """
        Checks for collision with a player and inflicts damage.

        If a collision is detected, the player takes damage and the projectile is removed.

        Parameters
        ----------
        player : Player
            The player object to check collision against.
        """
        if pygame.sprite.collide_mask(self, player):
            player.take_damage(self.damage)
            self.kill()

    def draw(self):
        """
        Draws the projectile on the screen.
        """
        self.screen.blit(self.image, self.rect)
