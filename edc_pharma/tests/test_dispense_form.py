from datetime import datetime
from django.test import TestCase

from edc_constants.constants import YES, NO
from edc_pharma.models import TABLET, SYRUP, IV

from edc_pharma.forms import DispenseForm
from edc_pharma.tests.factories.factory import SiteFactory, PatientFactory, ProtocolFactory,\
    MedicationFactory


class TestDispenseTabletForm(TestCase):

    def setUp(self):
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
            'syrup_volume': None,
            'total_dosage_volume': None,
            'iv_duration': None,
            'times_per_day': 3,
            'iv_concentration': None,
            'prepared_datetime': datetime.today()}

    def test_valid_form(self):
        form = DispenseForm(data=self.data)
        self.assertTrue(form.is_valid)

    def test_validate_taking_not_syrup(self):
        """Test if the patient is not taking syrup"""
        self.data['syrup_volume'] = "10ml"
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should NOT enter syrup volume',
            dispense_form.errors.get('syrup_volume', []))

    def test_validate_taking_not_syrup_valid(self):
        """Test if the patient is not taking syrup"""
        self.data['dispense_type'] = TABLET
        self.data['syrup_volume'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should NOT enter syrup volume',
            dispense_form.errors.get('syrup_volume', []))

    def test_validate_taking_right_amount_tablets(self):
        """Test if the patient is taking correct amount of tablets"""
        self.data['dispense_type'] = TABLET
        self.data['number_of_tablets'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should enter correct amount',
            dispense_form.errors.get('number_of_tablets', []))

    def test_validate_taking_tablet_at_right_time(self):
        """Test if the patient is taking tablets at right time"""
        self.data['tablet'] = YES
        self.data['times_per_day'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_validate_taking_iv(self):
        """Test if the patient is not taking iv within set time(minutes)"""
        self.data['tablet'] = YES
        self.data['iv_duration'] = NO
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should select dispense type iv',
            dispense_form.errors.get('iv_duration', []))

    def test_validate_iv_concentration(self):
        """Test if the patient is not taking iv within set time(minutes)"""
        self.data['tablet'] = YES
        self.data['iv_concentration'] = NO
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should select dispense type iv',
            dispense_form.errors.get('iv_concentration', []))

    def test_validate_taking_syrup(self):
        """Test if the patient is not taking syrup"""
        self.data['syrup'] = YES
        self.data['syrup_volume'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should enter syrup volume',
            dispense_form.errors.get('syrup_volume', []))


class TestDispenseSyrupForm(TestCase):

    def setUp(self):
        self.protocol = ProtocolFactory()
        self.site = SiteFactory()
        self.patient = PatientFactory()
        self.medication = MedicationFactory()
        self.data = {
            'patient': self.patient.id,
            'medication': self.medication.id,
            'dispense_type': SYRUP,
            'number_of_tablets': None,
            'total_number_of_tablets': None,
            'syrup_volume': None,
            'total_dosage_volume': None,
            'iv_duration': None,
            'times_per_day': 3,
            'iv_concentration': None,
            'prepared_datetime': datetime.today()}

    def test_valid_form(self):
        form = DispenseForm(data=self.data)
        self.assertTrue(form.is_valid)

    def test_without_syrup_volume(self):
        """Test if the patient is taking syrup, when syrup volume isn't included"""
        self.data['total_dosage_volume'] = '250mL'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should enter syrup volume',
            dispense_form.errors.get('syrup_volume', []))

    def test_without_total_dosage_volume(self):
        """Test if the patient is taking syrup, when total syrup volume isn't included"""
        self.data['syrup_volume'] = '5mL'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should enter total dosage volume',
            dispense_form.errors.get('total_dosage_volume', []))

    def test_with_number_of_tablets(self):
        """Test if the patient is taking syrup, when number of tablets is included"""
        self.data['syrup_volume'] = '5mL'
        self.data['total_dosage_volume'] = '250mL'
        self.data['number_of_tablets'] = 10
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should NOT enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_with_total_number_of_tablets(self):
        """Test if the patient is taking syrup, when total number of tablets is included"""
        self.data['syrup_volume'] = '5mL'
        self.data['total_dosage_volume'] = '250mL'
        self.data['total_number_of_tablets'] = 40
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should NOT enter total number of tablets',
            dispense_form.errors.get('total_number_of_tablets', []))

    def test_with_iv_duration(self):
        """Test if the patient is taking syrup, when iv duration is included"""
        self.data['syrup_volume'] = '5mL'
        self.data['total_dosage_volume'] = '250mL'
        self.data['iv_duration'] = '50mL'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should NOT enter IV duration',
            dispense_form.errors.get('iv_duration', []))

    def test_without_times_per_day(self):
        """Test if the patient is taking syrup, when times per day isn't included"""
        self.data['syrup_volume'] = '5mL'
        self.data['total_dosage_volume'] = '250mL'
        self.data['times_per_day'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_with_iv_concentration(self):
        """Test if the patient is taking syrup, when iv concentration is included"""
        self.data['syrup_volume'] = '5mL'
        self.data['total_dosage_volume'] = '250mL'
        self.data['iv_concentration'] = '50mL'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should NOT enter IV concentration',
            dispense_form.errors.get('iv_concentration', []))
