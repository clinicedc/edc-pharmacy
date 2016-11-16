from django.test import TestCase
from django.utils import timezone

from ..choices import SOLUTION
from ..forms import DispenseForm

from .factories import SiteFactory, PatientFactory, ProtocolFactory, MedicationFactory


class TestDispenseSolutionForm(TestCase):

    def setUp(self):
        """Setup data with all required fields for DISPENSE TYPE: SOLUTION"""
        self.protocol = ProtocolFactory()
        self.site = SiteFactory()
        self.patient = PatientFactory()
        self.medication = MedicationFactory()
        self.data = {
            'patient': self.patient.id,
            'medication': self.medication.id,
            'dispense_type': SOLUTION,
            'number_of_tablets': None,
            'total_number_of_tablets': None,
            'dose': '5mL',
            'total_volume': '250mL',
            'duration': None,
            'times_per_day': 3,
            'concentration': '2.4g/mL',
            'weight': None,
            'prepared_datetime': timezone.now()}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = DispenseForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_without_dose(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with dose not included"""
        self.data['dose'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type solution, you should enter dose',
            dispense_form.errors.get('dose', []))

    def test_with_dose(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with volume included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type solution, you should enter dose',
            dispense_form.errors.get('dose', []))

    def test_without_total_volume(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with total volume not included"""
        self.data['total_volume'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type solution, you should enter total volume',
            dispense_form.errors.get('total_volume', []))

    def test_with_total_volume(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with total volume included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type solution, you should enter total volume',
            dispense_form.errors.get('total_volume', []))

    def test_with_number_of_tablets(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with number of tablets included"""
        self.data['number_of_tablets'] = 10
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type solution, you should NOT enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_without_number_of_tablets(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with number of tablets not included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type solution, you should NOT enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_with_total_number_of_tablets(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with total number of tablets included"""
        self.data['total_number_of_tablets'] = 40
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type solution, you should NOT enter total number of tablets',
            dispense_form.errors.get('total_number_of_tablets', []))

    def test_without_total_number_of_tablets(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with total number of tablets included"""
        self.data['total_number_of_tablets'] = 40
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type solution, you should NOT enter total number of tablets',
            dispense_form.errors.get('total_number_of_tablets', []))

    def test_with_duration(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with duration included"""
        self.data['duration'] = '2 hours'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type solution, you should NOT enter duration',
            dispense_form.errors.get('duration', []))

    def test_without_duration(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with IV duration not included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type solution, you should NOT enter duration',
            dispense_form.errors.get('duration', []))

    def test_without_times_per_day(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with times per day not included"""
        self.data['times_per_day'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type solution, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_with_times_per_day(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with times per day included"""
        self.data['times_per_day'] = 3
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type solution, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_without_concentration(self):
        """Test when DISPENSE TYPE:SOLUTION is chosen with concentration not included"""
        self.data['concentration'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type solution, you should enter concentration',
            dispense_form.errors.get('concentration', []))
