from weapon import Weapon


class WeaponTemplate(Weapon):
    def __init__(self, position, groups):
        super().__init__(groups)
