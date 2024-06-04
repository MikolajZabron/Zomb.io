from utilities.graphical_object import Object


class Weapon(Object):
    """
    Represents a weapon object in the game.
    """

    def __init__(self, position, groups):
        """
        Initializes a Weapon object.

        Args:
            position (tuple): The initial position of the weapon.
            groups (tuple): The groups to which the weapon object belongs.
        """
        super().__init__(groups)
