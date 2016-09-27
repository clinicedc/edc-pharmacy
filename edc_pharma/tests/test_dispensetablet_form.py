from datetime import datetime
from django.test import TestCase

from edc_constants.constants import YES, NO
from edc_pharma.models import TABLET, SYRUP, IV

from edc_pharma.forms import DispenseForm
from edc_pharma.models import Dispense, Protocol, Site, Patient, Medication
from edc_pharma.tests.factories.patient_factory import PatientFactory, SiteFactory


class TestDispenseTabletForm(TestCase):

    def setUp(self):
        self.protocol = Protocol.objects.create(number='BHP001', name='001')
        self.site = SiteFactory()
        self.patient = PatientFactory()
        self.medication = Medication.objects.create(
            name='compral',
            protocol=self.protocol,
            storage_instructions='store at 5 deg centigrade')
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
            self.data['dispense_type'] = TABLET
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
        self.assertNotIn('You have selected dispense type tablet, you should select dispense type iv',
                         dispense_form.errors.get('iv_duration', []))

    def test_validate_iv_concentration(self):
        """Test if the patient is not taking iv within set time(minutes)"""
        self.data['tablet'] = YES
        self.data['iv_concentration'] = NO
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type tablet, you should select dispense type iv',
                         dispense_form.errors.get('iv_concentration', []))

    def test_validate_taking_syrup(self):
        """Test if the patient is not taking syrup"""
        self.data['syrup'] = YES
        self.data['syrup_volume'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type syrup, you should enter syrup volume',
                         dispense_form.errors.get('syrup_volume', []))
