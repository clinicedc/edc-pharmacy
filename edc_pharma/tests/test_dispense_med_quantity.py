from datetime import datetime
from edc_pharma.import_medication_list import medications

from django.test import TestCase, tag

from ..medications import DispenseMedQuantity


@tag('med')
class TestDispenseMedQuantity(TestCase):

    def test_repr(self):
        amphotericin = medications.get('amphotericin')
        med = DispenseMedQuantity(medication=amphotericin)
        self.assertTrue(med.__repr__())

    def test_quantity(self):
        amphotericin = medications.get('amphotericin')
        med = DispenseMedQuantity(
            medication=amphotericin, weight=32, duration=7)
        self.assertEqual(med.total_quantity, 5)
        self.assertEqual(med.medication.amount, 50)

    def test_quantity_1(self):
        flucytosine = medications.get('flucytosine')
        med = DispenseMedQuantity(
            medication=flucytosine, weight=32, duration=7)
        self.assertEqual(med.total_quantity, 45)
        self.assertEqual(med.medication.amount, 500)

    def test_quantity_2(self):
        flucytosine = medications.get('ambisome')
        med = DispenseMedQuantity(
            medication=flucytosine, weight=32, duration=7)
        self.assertEqual(med.total_quantity, 5)
        self.assertEqual(med.medication.amount, 500)
