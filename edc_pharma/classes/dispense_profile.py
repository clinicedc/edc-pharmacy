

class DispenseProfile:

    """A container class for medication type.
    """

    def __init__(self, name=None):
        self.name = name
        self.medication_types = {}

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.name})'

    def __str__(self):
        return self.name

    def add_medication_type(self, medication_type):
        """Adds a medication type instance to the profile.
        """
        self.medication_types.update({medication_type.name: medication_type})

    def get_medication_type(self, name=None):
        """ Returns a medication type instance using name.
        """
        return self.medication_types.get(name)
