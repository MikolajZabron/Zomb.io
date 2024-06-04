from utilities.settings import *
from utilities.graphical_object import Object


class Player(Object):
    """
    Represents the player character in the game.

    This class inherits from Object and defines behavior specific to the player character,
    such as movement, collision detection, health management, leveling up, and gaining experience.

    Attributes:
        animation_frames (list): List of frames for player animation.
        image (pygame.Surface): The image representing the player character.
        original_ratio (float): The original aspect ratio of the player character's image.
        rect (pygame.Rect): The rectangular area occupied by the player character.
        old_x (int): The previous x-coordinate of the player character.
        old_y (int): The previous y-coordinate of the player character.
        screen (pygame.Surface): The game screen surface.
        direction (pygame.math.Vector2): The direction of movement for the player.
        mask (pygame.Mask): The collision mask for the player character.
        exp (int): The current experience points of the player.
        target_exp (int): The target experience points for the player to level up.
        exp_need (int): The experience points needed for the player to level up.
        level (int): The current level of the player.
        whole_exp (int): The total accumulated experience points of the player.
        speed (int): The movement speed of the player.
        attack_speed (int): The attack speed of the player.
        damage (int): The overall damage dealt by the player.
        ranged_damage (int): The damage dealt by ranged attacks of the player.
        melee_damage (int): The damage dealt by melee attacks of the player.
        health (int): The current health points of the player.
        health_max (int): The maximum health points of the player.
        target_health (int): The target health points of the player.
        melee_range (int): The range of melee attacks of the player.
        bullet_range (int): The range of bullet attacks of the player.
        range (int): The range attribute of the player.
        ranged_weapons (int): The number of ranged weapons the player possesses.
        melee_weapons (int): The number of melee weapons the player possesses.
        frame_rate (int): The frame rate of the player animation.
        current_frame (int): The index of the current animation frame.
        last_update_time (int): The time of the last animation frame update.
        end_game (bool): Flag indicating if the game should end.
        not_moving (bool): Flag indicating if the player is not moving.

    Methods:
        __init__(position, groups, animation_frames): Constructor method for the Player class.
        input(): Handles player input for movement.
        update(structures, borders): Updates the player's position and checks for collisions.
        take_damage(amount): Inflicts damage to the player.
        collide_with_structures(structures): Handles collision with structures.
        collide_with_map_borders(borders): Handles collision with map borders.
        gain_experience(amount): Increases the player's experience points.
        level_up(): Levels up the player character.
        skill_choice(i): Handles skill choices for leveling up.
        raise_hp(): Increases the player's maximum health.
        restore_hp(): Restores missing health to the player.
        raise_melee_dmg(): Increases melee damage.
        raise_range_dmg(): Increases ranged damage.
        raise_range(): Increases player's range.
        raise_speed(): Increases player's movement speed.
        raise_atk_speed(): Increases player's attack speed.
        add_range(): Adds a new ranged weapon.
        add_melee(): Adds a new melee weapon.
        draw(): Draws the player character on the game screen.
        update_animation(): Updates the player character's animation.
    """

    def __init__(self, position, groups, animation_frames):
        """
        Constructor method for the Player class.

        Args:
            position (tuple): The initial position of the player.
            groups (pygame.sprite.AbstractGroup): The groups to which the player belongs.
            animation_frames (list): List of frames for player animation.
        """
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

        # Experience and leveling
        self.exp = PLAYER_EXPERIENCE
        self.target_exp = PLAYER_EXPERIENCE
        self.exp_need = PLAYER_EXPERIENCE_NEED
        self.level = PLAYER_LEVEL
        self.whole_exp = 0

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
        self.range = 1
        self.ranged_weapons = 1
        self.melee_weapons = 0

        # Animation stuff
        self.frame_rate = 10
        self.current_frame = 0
        self.last_update_time = pygame.time.get_ticks()
        self.end_game = False
        self.not_moving = True

    def input(self):
        """
        Handles player input for movement.
        """
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
        """
        Updates the player's position and checks for collisions.

        Args:
            structures: List of structures in the game.
            borders: List of map borders.
        """
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
        """
        Inflicts damage to the player.

        Args:
            amount (int): The amount of damage to be inflicted.
        """
        if self.target_health > 0:
            self.target_health -= amount
        else:
            self.target_health = 0
            self.end_game = True

    def collide_with_structures(self, structures):
        """
        Handles collision with structures.

        Args:
            structures: List of structures in the game.
        """
        for structure in structures:
            if pygame.sprite.collide_mask(self, structure):
                self.rect.center = self.old_x, self.old_y

    def collide_with_map_borders(self, borders):
        """
        Handles collision with map borders.

        Args:
            borders: List of map borders.
        """
        if ((self.rect.x < 620 - 1600) or (self.rect.x > 2550 - 1600) or (self.rect.y < 460 - 1200) or
                (self.rect.y > 1875 - 1200)):
            self.rect.center = self.old_x, self.old_y
        for border in borders:
            if pygame.sprite.collide_mask(self, border):
                self.rect.center = self.old_x, self.old_y

    def gain_experience(self, amount):
        """
        Increases the player's experience points.

        Args:
            amount (int): The amount of experience points gained.
        """
        self.target_exp += amount
        self.whole_exp += amount

    def level_up(self):
        """
        Levels up the player character.
        """
        self.exp -= self.exp_need
        self.target_exp = self.exp
        self.level += 1
        self.exp_need *= 1.2

    def skill_choice(self, i):
        """
        Handles skill choices for leveling up.

        Args:
            i (str): The skill choice.
        """
        if i == "ranged_weapon":  # Add new ranged weapon
            self.add_range()
        if i == "melee_weapon":  # Add new melee weapon
            self.add_melee()
        if i == "hp_max":  # Increase maximum hp
            self.raise_hp()
        if i == "hp_res":  # Restores missing health
            self.restore_hp()
        if i == "melee_dmg":  # Increase damage done by melee weapons
            self.raise_melee_dmg()
        if i == "range_dmg":  # Increase damage done by range weapons
            self.raise_range_dmg()
        if i == "range":  # Increase player range
            self.raise_range()
        if i == "speed":  # Increase player speed
            self.raise_speed()
        if i == "atk_speed":  # Increase attack speed
            self.raise_atk_speed()

    def raise_hp(self):
        """
        Increases the player's maximum health.
        """
        print(self.health_max)
        self.health_max += self.health_max * 0.2
        self.target_health += self.health_max * 0.2
        print(self.health_max)

    def restore_hp(self):
        """
        Restores missing health to the player.
        """
        self.target_health += self.health_max * 0.5

    def raise_melee_dmg(self):
        """
        Increases melee damage.
        """
        print(self.melee_damage)
        self.melee_damage += 2
        print(self.melee_damage)

    def raise_range_dmg(self):
        """
        Increases ranged damage.
        """
        print(self.ranged_damage)
        self.ranged_damage += 2
        print(self.ranged_damage)

    def raise_range(self):
        """
        Increases player's range.
        """
        print(self.range)
        self.range += 2
        print(self.range)

    def raise_speed(self):
        """
        Increases player's movement speed.
        """
        print(self.speed)
        self.speed += self.speed * 0.2
        print(self.speed)

    def raise_atk_speed(self):
        """
        Increases player's attack speed.
        """
        print(self.attack_speed)
        self.attack_speed += self.attack_speed * 0.2
        print(self.attack_speed)

    def add_range(self):
        """
        Adds a new ranged weapon.
        """
        self.ranged_weapons += 1

    def add_melee(self):
        """
        Adds a new melee weapon.
        """
        self.melee_weapons += 1

    def draw(self):
        """
        Draws the player character on the game screen.
        """
        self.screen.blit(self.image, self.rect)

    def update_animation(self):
        """
        Updates the player character's animation.
        """
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
