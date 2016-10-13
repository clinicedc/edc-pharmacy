from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.test import TestCase

from edc_pharma.models import TABLET, SYRUP, IV, IM, CAPSULES, SOLUTION
from edc_pharma.forms import DispenseForm
from edc_pharma.tests.factories.factory import SiteFactory, PatientFactory, ProtocolFactory,\
    MedicationFactory, DispenseFactory


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
            'syrup_dose': None,
            'total_dosage_volume': None,
            'iv_duration': None,
            'times_per_day': 3,
            'concentration': None,
            'prepared_datetime': datetime.today()}

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

    def test_with_syrup_dose(self):
        """Test when DISPENSE TYPE:TABLET is chosen with syrup dose included"""
        self.data['syrup_dose'] = "10ml"
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should NOT enter syrup dose',
            dispense_form.errors.get('syrup_dose', []))

    def test_without_syrup_dose(self):
        """Test when DISPENSE TYPE:TABLET is chosen with syrup volume not included"""
        self.data['syrup_volume'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should NOT enter syrup dose',
            dispense_form.errors.get('syrup_volume', []))

    def test_with_iv_duration(self):
        """Test when DISPENSE TYPE:TABLET is chosen and IV duration is included"""
        self.data['iv_duration'] = '2 hours'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should NOT enter IV duration',
            dispense_form.errors.get('iv_duration', []))

    def test_without_iv_duration(self):
        """Test when DISPENSE TYPE:TABLET is chosen and IV duration is included"""
        self.data['iv_duration'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should NOT enter IV duration',
            dispense_form.errors.get('iv_duration', []))

#     def test_with_iv_concentration(self):
#         """Test when DISPENSE TYPE:TABLET is chosen and concentration is included"""
#         self.data['concentration'] = '2mg/L'
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type tablet, you should NOT enter concentration',
#             dispense_form.errors.get('concentration', []))

#     def test_without_iv_concentration(self):
#         """Test when DISPENSE TYPE:TABLET is chosen and  concentration is included"""
#         self.data['concentration'] = None
#         dispense_form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type tablet, you should NOT enter concentration',
#             dispense_form.errors.get('concentration', []))

    def test_with_total_dosage_volume(self):
        """Test when DISPENSE TYPE:TABLET is chosen and total dosage volume is included"""
        self.data['total_dosage_volume'] = '300mL'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should NOT enter total dosage volume',
            dispense_form.errors.get('total_dosage_volume', []))

    def test_without_total_dosage_volume(self):
        """Test when DISPENSE TYPE:TABLET is chosen and total dosage volume is included"""
        self.data['total_dosage_volume'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type tablet, you should NOT enter total dosage volume',
            dispense_form.errors.get('total_dosage_volume', []))

    def test_without_times_per_day(self):
        """Test when DISPENSE TYPE: TABLET is chosen, you should enter times per day """
        self.data['times_per_day'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type tablet, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))


class TestDispenseSyrupForm(TestCase):

    def setUp(self):
        """Setup data with all required fields for DISPENSE TYPE: TABLET"""
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
            'syrup_dose': '5mL',
            'total_dosage_volume': '250mL',
            'iv_duration': None,
            'times_per_day': 3,
            'concentration': None,
            'prepared_datetime': datetime.today()}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = DispenseForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_without_syrup_volume(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with syrup dose not included"""
        self.data['syrup_dose'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should enter syrup dose',
            dispense_form.errors.get('syrup_dose', []))

    def test_with_syrup_volume(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with syrup volume included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should enter syrup volume',
            dispense_form.errors.get('syrup_dose', []))

    def test_without_total_dosage_volume(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with total dosage volume not included"""
        self.data['total_dosage_volume'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should enter total dosage volume',
            dispense_form.errors.get('total_dosage_volume', []))

    def test_with_total_dosage_volume(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with total dosage volume included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should enter total dosage volume',
            dispense_form.errors.get('total_dosage_volume', []))

    def test_with_number_of_tablets(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with number of tablets included"""
        self.data['number_of_tablets'] = 10
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should NOT enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_without_number_of_tablets(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with number of tablets not included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should NOT enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_with_total_number_of_tablets(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with total number of tablets included"""
        self.data['total_number_of_tablets'] = 40
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should NOT enter total number of tablets',
            dispense_form.errors.get('total_number_of_tablets', []))

    def test_without_total_number_of_tablets(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with total number of tablets included"""
        self.data['total_number_of_tablets'] = 40
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should NOT enter total number of tablets',
            dispense_form.errors.get('total_number_of_tablets', []))

    def test_with_iv_duration(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with IV duration included"""
        self.data['iv_duration'] = '2 hours'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should NOT enter IV duration',
            dispense_form.errors.get('iv_duration', []))

    def test_without_iv_duration(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with IV duration not included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should NOT enter IV duration',
            dispense_form.errors.get('iv_duration', []))

    def test_without_times_per_day(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with times per day not included"""
        self.data['times_per_day'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type syrup, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_with_times_per_day(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with times per day included"""
        self.data['times_per_day'] = 3
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type syrup, you should enter times per day',
            dispense_form.errors.get('times_per_day', []))

#     def test_with_iv_concentration(self):
#         """Test when DISPENSE TYPE:SYRUP is chosen with concentration not included"""
#         self.data['concentration'] = '50mg/L'
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type syrup, you should NOT enter concentration',
#             dispense_form.errors.get('concentration', []))
# 
#     def test_without_iv_concentration(self):
#         """Test when DISPENSE TYPE:SYRUP is chosen with concentration not included"""
#         dispense_form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type syrup, you should NOT enter concentration',
#             dispense_form.errors.get('concentration', []))


class TestDispenseIVForm(TestCase):
    """Setup data with all required fields for DISPENSE TYPE: IV"""
    def setUp(self):
        self.protocol = ProtocolFactory()
        self.site = SiteFactory()
        self.patient = PatientFactory()
        self.medication = MedicationFactory()
        self.data = {
            'patient': self.patient.id,
            'medication': self.medication.id,
            'dispense_type': IV,
            'number_of_tablets': None,
            'total_number_of_tablets': None,
            'syrup_dose': None,
            'total_dosage_volume': '3000mL',
            'iv_duration': '2hours',
            'times_per_day': None,
            'concentration': '3mg/L',
            'prepared_datetime': datetime.today()}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = DispenseForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_with_number_of_tablets(self):
        """Test when DISPENSE TYPE:IV is chosen with number of tablets included"""
        self.data['number_of_tablets'] = 1
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type IV, you should NOT enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_without_number_of_tablets(self):
        """Test when DISPENSE TYPE:IV is chosen with number of tablets not included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type IV, you should NOT enter number of tablets',
            dispense_form.errors.get('number_of_tablets', []))

    def test_with_syrup_volume(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with syrup dose included"""
        self.data['syrup_dose'] = '5mL'
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type IV, you should NOT enter syrup dose',
            dispense_form.errors.get('syrup_dose', []))

    def test_without_syrup_volume(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with syrup dose not included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type IV, you should NOT enter syrup dose',
            dispense_form.errors.get('syrup_dose', []))

    def test_without_total_dosage_volume(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with total dosage volume not included"""
        self.data['total_dosage_volume'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type IV, you should enter total dosage volume',
            dispense_form.errors.get('total_dosage_volume', []))

    def test_with_total_dosage_volume(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with total dosage volume included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type IV, you should enter total dosage volume',
            dispense_form.errors.get('total_dosage_volume', []))

    def test_without_iv_duration(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with IV duration not included"""
        self.data['iv_duration'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type IV, you should enter IV duration',
            dispense_form.errors.get('iv_duration', []))

    def test_with_iv_duration(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with IV duration not included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type IV, you should enter IV duration',
            dispense_form.errors.get('iv_duration', []))

    def test_with_times_per_day(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with times per day included"""
        self.data['times_per_day'] = 3
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type IV, you should NOT enter times per day',
            dispense_form.errors.get('times_per_day', []))

    def test_without_times_per_day(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with times per day not included"""
        self.data['times_per_day'] = 3
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type IV, you should NOT enter times per day',
            dispense_form.errors.get('times_per_day', []))
 
    def test_without_iv_concentration(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with concentration not included"""
        self.data['concentration'] = None
        dispense_form = DispenseForm(data=self.data)
        self.assertIn(
            'You have selected dispense type IV, you should enter IV concentration',
            dispense_form.errors.get('concentration', []))
 
    def test_with_iv_concentration(self):
        """Test when DISPENSE TYPE:SYRUP is chosen with concentration included"""
        dispense_form = DispenseForm(data=self.data)
        self.assertNotIn(
            'You have selected dispense type IV, you should enter IV concentration',
            dispense_form.errors.get('concentration', []))
 
 
class TestDispenseModel(TestCase):
    """Setup data with all required fields for DISPENSE TYPE: IV"""
    def setUp(self):
        self.protocol = ProtocolFactory()
        self.site = SiteFactory()
        self.patient = PatientFactory()
        self.medication = MedicationFactory()
        self.dispense = DispenseFactory(patient=self.patient, medication=self.medication)
        self.data = {
            'patient': self.patient.id,
            'medication': self.medication.id,
            'dispense_type': TABLET,
            'number_of_tablets': 1,
            'total_number_of_tablets': 30,
            'syrup_dose': None,
            'total_dosage_volume': None,
            'iv_duration': None,
            'times_per_day': 1,
            'concentration': None,
            'prepared_date': date.today(),
            'prepared_datetime': datetime.now()}
 
    def test_refill_date_logic(self):
        """Test to verify whether the refill date method returns the right date"""
        self.assertEqual(self.dispense.refill_date, date.today() + relativedelta(days=16))
 
    def test_unique_date_medication_patient(self):
        """Test to verify that unique integrity in fields: patient, medication, prepared_date is maintained"""
        form = DispenseForm(data=self.data)
        self.assertFalse(form.is_valid())
