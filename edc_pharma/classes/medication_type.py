

class MedicationType:
    """Represent a medication record.
    """

    def __init__(self, name=None, description=None, unit=None):
        self.name = name
        self.description = description
        self.unit = unit

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name} {self.unit})'
