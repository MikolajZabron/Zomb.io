from utilities.graphical_object import Object


class Structure(Object):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.rect = self.image.get_rect(center=position)
