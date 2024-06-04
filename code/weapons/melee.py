from utilities.settings import *
from utilities.graphical_object import Object


class Melee(Object):
    def __init__(self, player, enemy, groups):
        super().__init__(groups)
        self.image = MELEE_TEMPLATE
        self.original_ratio = self.image.get_width() / self.image.get_height()
        self.image = pygame.transform.scale(self.image, (100, 100 / self.original_ratio))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=player.rect.center)
        self.screen = pygame.display.get_surface()
        self.direction = pygame.math.Vector2()
        self.dealt_damage = False
        self.creation_time = pygame.time.get_ticks()

        self.angle = self.calculate_angle(player.rect.center, enemy.rect.center)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        offset_distance = 50
        offset_x = offset_distance * pygame.math.Vector2(1, 0).rotate(-self.angle).x
        offset_y = offset_distance * pygame.math.Vector2(1, 0).rotate(-self.angle).y
        self.rect.centerx += offset_x
        self.rect.centery += offset_y

    def deal_damage(self):
        self.dealt_damage = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self, *args, **kwargs):
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time >= 250 and self.deal_damage:
            print("kill")
            self.kill()

    def calculate_angle(self, player_pos, enemy_pos):
        # Calculate the angle between the player and the enemy
        dx = enemy_pos[0] - player_pos[0]
        dy = enemy_pos[1] - player_pos[1]
        return pygame.math.Vector2(dx, dy).angle_to(pygame.math.Vector2(1, 0))
