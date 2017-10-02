from django.test import TestCase, tag

from ..medication import MedicationType
from ..print_profile import DispenseProfile


@tag('DispenseProfile')
class TestDispenseProfile(TestCase):

    def test_dispense_profile(self):
        dispense_profile = DispenseProfile(name='enrollment_profile')
        self.assertTrue(dispense_profile)

    def test_add_medication_type(self):
        dispense_profile = DispenseProfile(name='enrollment_profile')
        medication_type = MedicationType(
            name='med1', description='med1-desc', unit='1000ML')
        dispense_profile.add_medication_type(medication_type)
        self.assertEqual(len(dispense_profile.medication_types), 1)

    def test_add_medication_type_more(self):
        """ Assert that more one medication type can be added to dispense profile.
        """
        dispense_profile = DispenseProfile(name='enrollment_profile')
        medication_type1 = MedicationType(
            name='med1', description='med1-desc', unit='1000ML')
        medication_type2 = MedicationType(
            name='med2', description='med2 description', unit='1000ML')
        dispense_profile.add_medication_type(medication_type1)
        dispense_profile.add_medication_type(medication_type2)
        self.assertEqual(len(dispense_profile.medication_types), 2)

    def test_update_medication_type(self):
        """ Assert that adding same medication type twice just update existing
        medication type.
        """
        dispense_profile = DispenseProfile(name='enrollment_profile')
        medication_type1 = MedicationType(
            name='med1', description='med1-desc', unit='1000ML')
        dispense_profile.add_medication_type(medication_type1)
        medication_type2 = MedicationType(
            name='med1', description='med1 description', unit='2000ML')
        dispense_profile.add_medication_type(medication_type2)
        med_type = dispense_profile.get_medication_type(name='med1')
        self.assertEqual(med_type.unit, '2000ML')
        self.assertEqual(med_type.description, 'med1 description')
