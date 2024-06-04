from utilities.settings import *
from utilities.graphical_object import Object


class Player(Object):

    def __init__(self, position, groups, animation_frames):
        super().__init__(groups)
        self.animation_frames: list = animation_frames
        self.image = self.animation_frames[0].convert_alpha()
        self.original_ratio = self.image.get_width() / self.image.get_height()
        self.image = pygame.transform.scale(self.image, (24, 24/self.original_ratio))
        self.rect = self.image.get_rect(center=position)
        self.old_x = 0
        self.old_y = 0
        self.screen = pygame.display.get_surface()
        self.direction = pygame.math.Vector2()
        self.mask = pygame.mask.from_surface(self.image)

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
        self.health = PLAYER_HEALTH
        self.health_max = PLAYER_MAX_HEALTH
        self.target_health = PLAYER_MAX_HEALTH
        self.melee_range = PLAYER_MELEE_RANGE
        self.bullet_range = PLAYER_BULLET_RANGE

        # Animation stuff
        self.frame_rate = 10
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.end_game = False
        self.not_moving = True

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

    def update(self, structures=None, borders=None):
        self.old_x, self.old_y = self.rect.center
        self.input()
        if self.direction.length() == 0:
            self.not_moving = True
        else:
            self.not_moving = False
        self.rect.center += self.direction * self.speed
        if structures:
            self.collide_with_structures(structures)
        if borders:
            self.collide_with_map_borders(borders)
        self.update_animation()

    def take_damage(self, amount):
        if self.target_health > 0:
            self.target_health -= amount
        else:
            self.target_health = 0
            self.end_game = True

    def collide_with_structures(self, structures):
        for structure in structures:
            if pygame.sprite.collide_mask(self, structure):
                self.rect.center = self.old_x, self.old_y

    def collide_with_map_borders(self, borders):
        if ((self.rect.x < 620 - 1600) or (self.rect.x > 2550 - 1600) or (self.rect.y < 460 - 1200) or
                (self.rect.y > 1875 - 1200)):
            self.rect.center = self.old_x, self.old_y
        for border in borders:
            if pygame.sprite.collide_mask(self, border):
                self.rect.center = self.old_x, self.old_y

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

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if not self.not_moving:
            if current_time - self.last_update_time > 1000 // self.frame_rate:
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
                self.image = self.animation_frames[self.current_frame].convert_alpha()
                self.image = pygame.transform.scale(self.image, (24, 24/self.original_ratio))
                self.mask = pygame.mask.from_surface(self.image)
                self.last_update_time = current_time
        else:
            self.image = self.animation_frames[0].convert_alpha()
            self.image = pygame.transform.scale(self.image, (24, 24/self.original_ratio))
            self.mask = pygame.mask.from_surface(self.image)
            self.last_update_time = current_time
