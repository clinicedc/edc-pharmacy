from django.test import TestCase

from ..medication import MedicationType
from ..print_profile import SiteDispenseProfiles
from ..print_profile.dispense_profile import DispenseProfile


class TestSiteDispenseProfiles(TestCase):

    def test_site_dispense_profiles_add(self):
        site_profiles = SiteDispenseProfiles()
        dispense_profile = DispenseProfile(
            name='enrollment', profile_type='control')
        medication_type = MedicationType(
            name='med1', description='med1-desc', unit='1000ML')
        dispense_profile.add_medication_type(medication_type)
        site_profiles.register(dispense_profile)
        self.assertEqual(len(site_profiles.profiles), 1)

    def test_get_dispense_profile(self):
        site_profiles = SiteDispenseProfiles()
        dispense_profile = DispenseProfile(
            name='enrollment', profile_type='control')
        medication_type = MedicationType(
            name='med1', description='med1-desc', unit='1000ML')
        dispense_profile.add_medication_type(medication_type)
        site_profiles.register(dispense_profile)
        profile_type = dispense_profile.profile_type
        dispense_profile = site_profiles.get(
            name=f'{dispense_profile.name}.{profile_type}')
        self.assertTrue(dispense_profile)

    def test_site_profiles_1(self):
        pass
