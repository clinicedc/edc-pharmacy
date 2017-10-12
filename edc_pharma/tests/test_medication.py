from datetime import datetime
from edc_pharma.medications import medications

from django.test import TestCase, tag

from ..medications import Medication


@tag('med')
class TestMedication(TestCase):

    def test_repr(self):
        amphotericin = medications.get('amphotericin')
        med = Medication(medication_definition=amphotericin)
        self.assertTrue(med.__repr__())

    def test_quantity(self):
        amphotericin = medications.get('amphotericin')
        med = Medication(
            medication_definition=amphotericin, weight=32, duration=7)
        self.assertEqual(med.required_quantity, 5)

    def test_quantity_1(self):
        flucytosine = medications.get('flucytosine')
        med = Medication(
            medication_definition=flucytosine, weight=32, duration=7)
        self.assertEqual(med.required_quantity, 45)

    def test_quantity_2(self):
        flucytosine = medications.get('ambisome')
        med = Medication(
            medication_definition=flucytosine, weight=32, duration=7)
        self.assertEqual(med.required_quantity, 5)
        self.assertEqual(med.definition.total, 500)
