from utilities.graphical_object import Object


class Enemy(Object):
    def __init__(self, groups):
        super().__init__(groups)
        self.health = 1

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def move(self):
        """TODO: write a algorithm for all enemies to move"""

    def bite(self):
        """TODO: method that makes the enemy deal damage to the player"""
