from utilities.settings import *
from utilities.graphical_object import Object


class BulletTemplate(Object):
    """
    Represents a template for bullets fired in the game.
    """

    def __init__(self, position, destination, groups):
        """
        Initializes a BulletTemplate object.

        Args:
            position (tuple): The initial position of the bullet.
            destination (tuple): The destination position of the bullet.
            groups (tuple): The groups to which the bullet belongs.
        """
        super().__init__(groups)
        self.image = BULLET_TEMPLATE_IMAGE.convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=position)
        self.screen = pygame.display.get_surface()
        self.destination = destination
        self.direction = pygame.math.Vector2()
        self.speed = BULLET_SPEED

    def collision(self, group, damage, player):
        """
        Checks for collision between the bullet and a group of sprites.

        Args:
            group (pygame.sprite.Group): The group of sprites to check for collision.
            damage (int): The damage inflicted by the bullet.
            player (Player): The player object.

        """
        for enemy in pygame.sprite.spritecollide(self, group, False):
            enemy.take_damage(damage + player.ranged_damage, player)
            self.kill()

    def update(self):
        """
        Updates the bullet's position.
        """
        direction = pygame.math.Vector2(self.destination[0] - self.rect.centerx,
                                        self.destination[1] - self.rect.centery)
        if direction.length() > 0:
            direction.normalize_ip()
            self.rect.move_ip(direction * self.speed)

        if (direction.x > 0 and self.rect.centerx >= self.destination[0]) or \
                (direction.x < 0 and self.rect.centerx <= self.destination[0]) or \
                (direction.y > 0 and self.rect.centery >= self.destination[1]) or \
                (direction.y < 0 and self.rect.centery <= self.destination[1]):
            self.kill()

    def draw(self):
        """
        Draws the bullet on the screen.
        """
        self.screen.blit(self.image, self.rect)
