from utilities.settings import *
from utilities.graphical_object import Object


class Player(Object):

    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = PLAYER_IMAGE.convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(topleft=position)
        self.old_x = 0
        self.old_y = 0
        self.screen = pygame.display.get_surface()
        self.direction = pygame.math.Vector2()

        self.exp = PLAYER_EXPERIENCE
        self.target_exp = PLAYER_EXPERIENCE
        self.exp_need = PLAYER_EXPERIENCE_NEED
        self.level = PLAYER_LEVEL

        # Statistics
        self.speed = PLAYER_SPEED
        self.attack_speed = PLAYER_ATTACK_SPEED
        self.damage = PLAYER_DAMAGE
        self.ranged_damage = PLAYER_RANGED_DAMAGE
        self.melee_damage = PLAYER_MELEE_DAMAGE
        self.engineer_damage = PLAYER_ENGINEER_DAMAGE
        self.health = PLAYER_HEALTH
        self.health_max = PLAYER_MAX_HEALTH
        self.target_health = PLAYER_MAX_HEALTH
        self.melee_range = PLAYER_MELEE_RANGE
        self.bullet_range = PLAYER_BULLET_RANGE

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def update(self, structures=None):
        self.old_x, self.old_y = self.rect.topleft
        self.input()
        self.rect.topleft += self.direction * self.speed
        if structures:
            self.collide_with_structures(structures)

    def take_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health <= 0:
            self.target_health = 0

    def collide_with_structures(self, structures):
        for structure in structures:
            if self.rect.colliderect(structure.rect):
                self.rect.topleft = self.old_x, self.old_y

    def gain_experience(self, amount):
        self.target_exp += amount

    def level_up(self):
        self.exp -= self.exp_need
        self.target_exp = self.exp
        self.level += 1
        self.exp_need *= 1.2

    def skill_choice(self, i):
        print(i)

    def draw(self):
        self.screen.blit(self.image, self.rect)
