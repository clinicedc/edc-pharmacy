from django.test import TestCase

from ..site_dispense_profiles import site_profiles
from edc_pharma.classes.dispense_profile import DispenseProfile
from edc_pharma.classes.medication_type import MedicationType


class TestSiteDispenseProfiles(TestCase):

    def test_site_dispense_profiles_add(self):
        dispense_profile = DispenseProfile(name='enrollment_profile')
        medication_type = MedicationType(
            name='med1', description='med1-desc', unit='1000ML')
        dispense_profile.add_medication_type(medication_type)
        site_profiles.register(dispense_profile)
        self.assertEqual(len(site_profiles.profiles), 1)

    def test_get_dispense_profile(self):
        dispense_profile = DispenseProfile(name='enrollment_profile')
        medication_type = MedicationType(
            name='med1', description='med1-desc', unit='1000ML')
        dispense_profile.add_medication_type(medication_type)
        site_profiles.register(dispense_profile)
        dispense_profile = site_profiles.get(name='enrollment_profile')
        self.assertTrue(dispense_profile)
