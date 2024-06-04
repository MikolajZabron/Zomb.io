from weapon import Weapon


class WeaponTemplate(Weapon):
    """
    Represents a template for creating new weapons.

    This class inherits from the Weapon class.
    """

    def __init__(self, position, groups):
        """
        Initializes a WeaponTemplate object.

        Args:
            position (tuple): The initial position of the weapon template.
            groups (tuple): The groups to which the weapon template object belongs.
        """
        super().__init__(groups)
