from ..medication import MedicationType
from ..print_profile import DispenseProfile


class SiteDispenseProfiles:

    """Registers all defined dispense profile for profiles.
    """

    def __init__(self):
        self._registry = {}

    def __repr__(self):
        return f'{self.__class__.__name__}(loaded={self.loaded})'

    def get(self, name=None):
        """ Returns a dispense profile for given dispense profile name.
        """
        return self._registry.get(name)

    def register(self, dispense_profile=None):
        """Registers a dispense profile instance using the dispense profile name
        as the key.
        """
        if dispense_profile:
            profile_type = dispense_profile.profile_type
            self._registry.update({
                f'{dispense_profile.name}.{profile_type}': dispense_profile})

    @property
    def profiles(self):
        """Returns all registered dispense profiles.
        """
        return self._registry


site_profiles = SiteDispenseProfiles()

ambisome = MedicationType(
    name='Ambisome',
    description='Ambisome 10 mg/kg/day',
    unit='10 mg/kg')
fluconazole = MedicationType(
    name='Fluconazole',
    description='fluconazole 1200mg/day',
    unit='1200mg')
flucytosine = MedicationType(
    name='Flucytosine',
    description='flucytosine 100mg',
    unit='100mg')
amphotericin = MedicationType(
    name='Amphotericin B',
    description='amphotericin B 1 mg/kg',
    unit='1 mg/kg')


single_dose_enrollment = DispenseProfile(
    name='enrollment', profile_type='single_dose')
single_dose_enrollment.add_medication_type(ambisome)
single_dose_enrollment.add_medication_type(fluconazole)
single_dose_enrollment.add_medication_type(flucytosine)
site_profiles.register(single_dose_enrollment)

single_dose_followup = DispenseProfile(
    name='followup', profile_type='single_dose')
single_dose_followup.add_medication_type(fluconazole)
single_dose_followup.add_medication_type(flucytosine)
site_profiles.register(single_dose_followup)

control_arm_enrollemnt = DispenseProfile(
    name='enrollment', profile_type='control_arm')
control_arm_enrollemnt.add_medication_type(amphotericin)
control_arm_enrollemnt.add_medication_type(flucytosine)
site_profiles.register(control_arm_enrollemnt)

control_followup_profile = DispenseProfile(
    name='followup', profile_type='control_arm')
control_followup_profile.add_medication_type(amphotericin)
control_followup_profile.add_medication_type(flucytosine)
site_profiles.register(control_followup_profile)
