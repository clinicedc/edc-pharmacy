from django.test import TestCase
from django.utils import timezone

from ..constants import TABLET
from ..forms import DispenseForm

from .factories import SiteFactory, PatientFactory, ProtocolFactory, MedicationFactory


class TestDispenseTabletForm(TestCase):

    def setUp(self):
        """Setup data with all required fields for DISPENSE TYPE: TABLET"""
        self.protocol = ProtocolFactory()
        self.site = SiteFactory()
        self.patient = PatientFactory()
        self.medication = MedicationFactory()
        self.data = {
            'patient': self.patient.id,
            'medication': self.medication.id,
            'dispense_type': TABLET,
            'number_of_tablets': 1,
            'total_number_of_tablets': 30,
            'dose': None,
            'total_volume': None,
            'duration': None,
            'times_per_day': 3,
            'concentration': '3.5mg/mL',
            'weight': None,
            'prepared_datetime': timezone.now()}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = DispenseForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_with_number_of_tablets(self):
        """Test when DISPENSE TYPE:TABLET is chosen with number of tablets included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_without_number_of_tablets(self):
        """Test when DISPENSE TYPE:TABLET is chosen with number of tablets not included"""
        self.data['number_of_tablets'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_without_total_number_of_tablets(self):
        """Test when DISPENSE TYPE:TABLET is chosen with total number of tablets not included"""
        self.data['total_number_of_tablets'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should enter total number of tablets',
            dispense_form.errors.get('total_number_of_tablets', []))

    def test_with_total_number_of_tablets(self):
        """Test when DISPENSE TYPE:TABLET is chosen with total number of tablets included"""
        self.data['total_number_of_tablets'] = 40
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should enter total number of tablets',
            dispense_form.errors.get('total_number_of_tablets', []))

    def test_with_dose(self):
        """Test when DISPENSE TYPE:TABLET is chosen with syrup dose included"""
        self.data['dose'] = "10ml"
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should NOT enter dose',
            dispense_form.errors.get('dose', []))

    def test_without_dose(self):
        """Test when DISPENSE TYPE:TABLET is chosen with syrup volume not included"""
        self.data['dose'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should NOT enter dose',
            dispense_form.errors.get('dose', []))

    def test_with_duration(self):
        """Test when DISPENSE TYPE:TABLET is chosen and IV duration is included"""
        self.data['duration'] = '2 hours'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should NOT enter duration',
            dispense_form.errors.get('duration', []))

    def test_without_duration(self):
        """Test when DISPENSE TYPE:TABLET is chosen and IV duration is included"""
        self.data['duration'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should NOT enter IV duration',
            dispense_form.errors.get('duration', []))

    def test_with_total_volume(self):
        """Test when DISPENSE TYPE:TABLET is chosen and total dosage volume is included"""
        self.data['total_volume'] = '300mL'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should NOT enter total volume',
            dispense_form.errors.get('total_volume', []))

    def test_without_total_volume(self):
        """Test when DISPENSE TYPE:TABLET is chosen and total dosage volume is included"""
        self.data['total_volume'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should NOT enter total volume',
            dispense_form.errors.get('total_volume', []))

    def test_without_concentration(self):
        """Test when DISPENSE TYPE:TABLET is chosen with concentration not included"""
        self.data['concentration'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should enter concentration',
            dispense_form.errors.get('total_volume', []))

    def test_without_times_per_day(self):
        """Test when DISPENSE TYPE: TABLET is chosen and times per day is not included"""
        self.data['times_per_day'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_with_weight(self):
        """Test when DISPENSE TYPE: TABLET is chosen and weight is included"""
        self.data['weight'] = 2.6
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should NOT enter weight',
            dispense_form.errors.get('weight', []))
