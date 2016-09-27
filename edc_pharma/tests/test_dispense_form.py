from datetime import datetime
from django.test import TestCase

from edc_constants.constants import NO
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
            'number_of_tablets': 2,
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

    def test_validate_taking_right_amount_tablets_valid(self):
        """Test if the patient is taking correct amount of tablets"""
        self.data['dispense_type'] = TABLET
        self.data['number_of_tablets'] = 2
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should enter total number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

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
        self.data['dispense_type'] = TABLET
        self.data['times_per_day'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_validate_taking_iv(self):
        """Test if the patient is not taking iv within set time(minutes)"""
        self.data['dispense_type'] = TABLET
        self.data['iv_duration'] = NO
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type tablet, you should select dispense type iv',
                         dispense_form.errors.get('iv_duration', []))

    def test_validate_iv_concentration(self):
        """Test if the patient is not taking iv within set time(minutes)"""
        self.data['dispense_type'] = TABLET
        self.data['iv_concentration'] = NO
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type tablet, you should select dispense type iv',
                         dispense_form.errors.get('iv_concentration', []))

    def test_validate_taking_syrup(self):
        """Test if the patient is not taking syrup"""
        self.data['dispense_type'] = SYRUP
        self.data['syrup_volume'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertIn('You have selected dispense type syrup, you should enter syrup volume',
                      dispense_form.errors.get('syrup_volume', []))

    def test_validate_taking_syrup_volume(self):
        """Test if the patient is not entering the number of tablets"""
        self.data['dispense_type'] = SYRUP
        self.data['number_of_tablets'] = 2
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type syrup, you should NOT enter number of tablets',
                         dispense_form.errors.get('number_of_tablets', []))

    def test_entering_right_dosage_volume(self):
        """Test if the patient is not taking right dosage"""
        self.data['dispense_type'] = SYRUP
        self.data['total_dosage_volume'] = '20ml'
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type syrup, you should enter total dosage volume',
                         dispense_form.errors.get('total_dosage_volume', []))

    def test_entering_iv_concentration_is_valid(self):
        """Test if the patient is not entering iv_concentration"""
        self.data['dispense_type'] = SYRUP
        self.data['iv_concentration'] = '20ml'
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type syrup, you should NOT enter IV concentration',
                         dispense_form.errors.get('iv_concentration', []))

    def test_entering_times_per_day_of_syrup_is_valid(self):
        """Test if the patient is not entering the number of taking syrup per day"""
        self.data['dispense_type'] = SYRUP
        self.data['times_per_day'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type syrup, you should enter times per day',
                         dispense_form.errors.get('times_per_day', []))

    def test_without_total_dosage_volume(self):
        """Test if the patient is taking syrup, when total syrup volume isn't included"""
        self.data['syrup_volume'] = '5mL'
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should enter total dosage volume',
            dispense_form.errors.get('total_dosage_volume', []))

    def test_with_iv_duration(self):
        """Test if the patient is taking syrup, when iv duration is not included"""
        self.data['syrup_volume'] = '5mL'
        self.data['total_dosage_volume'] = '250mL'
        self.data['iv_duration'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should enter IV duration',
            dispense_form.errors.get('iv_duration', []))

    def test_without_times_per_day(self):
        """Test if the patient is taking syrup, when times per day isn't included"""
        self.data['syrup_volume'] = '5mL'
        self.data['total_dosage_volume'] = '250mL'
        self.data['times_per_day'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_validate_taking_not_iv(self):
            """Test if the patient is not taking iv"""
            self.data['dispense_type'] = IV
            self.data['syrup_volume'] = 0
            dispense_form = DispenseForm(data=self.data)
            self.assertNotIn(
                'You have selected dispense type iv, you should NOT enter syrup volume',
                dispense_form.errors.get('syrup_volume', []))

    def test_validate_taking_right_amount_tablets_not_valid(self):
        """Test if the patient is taking correct amount of tablets"""
        self.data['dispense_type'] = IV
        self.data['number_of_tablets'] = 2
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type IV, you should NOT enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_validate_taking_iv_valid(self):
        """Test if the patient is not taking iv"""
        self.data['dispense_type'] = IV
        self.data['total_dosage_volume'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type syrup, you should enter total_dosage_volume',
                         dispense_form.errors.get('total_dosage_volume', []))

    def test_validate_taking_iv_duration_valid(self):
        """Test if the patient is not taking iv"""
        self.data['dispense_type'] = IV
        self.data['iv_duration'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type iv, you should enter iv_duration',
                         dispense_form.errors.get('iv_duration', []))

    def test_validate_taking_iv_concentration_valid(self):
        """Test if the patient is taking correct iv_concentration"""
        self.data['dispense_type'] = IV
        self.data['iv_concentration'] = 0
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type iv, you should enter correct iv_concentration',
                         dispense_form.errors.get('iv_concentration', []))

    def test_validate_taking_total_number_of_tablets_not_valid(self):
        """Test if the patient is taking correct iv_concentration"""
        self.data['dispense_type'] = IV
        self.data['total_number_of_tablets'] = 2
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type iv, you should not enter total_number_of_tablets',
                         dispense_form.errors.get('total_number_of_tablets', []))

    def test_validate_taking_tables_times_per_day_not_valid(self):
        """Test if the patient is taking correct iv_concentration"""
        self.data['dispense_type'] = IV
        self.data['times_per_day'] = 3
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn('You have selected dispense type IV, you should NOT enter times per day',
                         dispense_form.errors.get('times_per_day', []))
