

class SiteDispenseProfiles:

    """Registers all defined dispense profile for profiles.
    """

    def __init__(self):
        self._registry = {}

    def __repr__(self):
        return f'{self.__class__.__name__}(loaded={self.loaded})'

    def get(self, name):
        """ Returns a dispense profile for given dispense profile name.
        """
        return self._registry.get(name)

    def register(self, dispense_profile=None):
        """Registers a dispense profile instance using the dispense profile name
        as the key.
        """
        if dispense_profile:
            self._registry.update({dispense_profile.name: dispense_profile})

    @property
    def profiles(self):
        """Returns all registered dispense profiles.
        """
        return self._registry


site_profiles = SiteDispenseProfiles()
