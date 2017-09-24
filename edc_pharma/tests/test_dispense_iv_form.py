# from django.test import TestCase
# from django.utils import timezone
# 
# 
# from ..constants import IV
# from ..forms import DispenseForm
# 
# from .factories import SiteFactory, PatientFactory, ProtocolFactory, MedicationFactory
# 
# 
# class TestDispenseIVForm(TestCase):
#     """Setup data with all required fields for DISPENSE TYPE: IV"""
#     def setUp(self):
#         self.protocol = ProtocolFactory()
#         self.site = SiteFactory()
#         self.patient = PatientFactory()
#         self.medication = MedicationFactory()
#         self.data = {
#             'patient': self.patient.id,
#             'medication': self.medication.id,
#             'dispense_type': IV,
#             'number_of_tablets': None,
#             'total_number_of_tablets': None,
#             'dose': None,
#             'total_volume': '3000mL',
#             'infusion_number': None,
#             'duration': '2hours',
#             'times_per_day': None,
#             'concentration': '3mg/L',
#             'weight': 2.6,
#             'prepared_datetime': timezone.now()}
# 
#     def test_valid_form(self):
#         """Test to verify whether form will submit"""
#         form = DispenseForm(data=self.data)
#         self.assertTrue(form.is_valid())
# 
#     def test_with_times_per_day(self):
#         """Test when DISPENSE TYPE:IV is chosen with times per day included"""
#         self.data['times_per_day'] = 2
#         form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type IV, you should NOT enter times per day',
#             form.errors.get('times_per_day', []))
# 
#     def test_without_times_per_day(self):
#         """Test when DISPENSE TYPE:IV is chosen with times per day not included"""
#         form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type IV, you should NOT enter times per day',
#             form.errors.get('times_per_day', []))
# 
#     def test_without_total_volume(self):
#         """Test when DISPENSE TYPE:IV is chosen with total volume not included"""
#         self.data['total_volume'] = None
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type IV, you should enter total volume',
#             dispense_form.errors.get('total_volume', []))
# 
#     def test_with_total_volume(self):
#         """Test when DISPENSE TYPE:IV is chosen with total volume included"""
#         dispense_form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type IV, you should enter total volume',
#             dispense_form.errors.get('total_volume', []))
# 
#     def test_without_duration(self):
#         """Test when DISPENSE TYPE:IV is chosen with duration not included"""
#         self.data['duration'] = None
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type IV, you should enter duration',
#             dispense_form.errors.get('duration', []))
# 
#     def test_with_duration(self):
#         """Test when DISPENSE TYPE:IV is chosen with duration included"""
#         dispense_form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type IV, you should enter duration',
#             dispense_form.errors.get('duration', []))
# 
#     def test_with_number_of_tablets(self):
#         """Test when DISPENSE TYPE:IV is chosen with number of tablets included"""
#         self.data['number_of_tablets'] = 1
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type IV, you should NOT enter number of tablets',
#             dispense_form.errors.get('number_of_tablets', []))
# 
#     def test_with_total_number_of_tablets(self):
#         """Test when DISPENSE TYPE:IV is chosen with total number of tablets included"""
#         self.data['total_number_of_tablets'] = 30
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type IV, you should NOT enter total number of tablets',
#             dispense_form.errors.get('total_number_of_tablets', []))
# 
#     def test_without_concentration(self):
#         """Test when DISPENSE TYPE: IV is chosen with concentration not included"""
#         self.data['concentration'] = None
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type IV, you should enter concentration',
#             dispense_form.errors.get('concentration', []))
# 
#     def test_with_concentration(self):
#         """Test when DISPENSE TYPE: IV is chosen with concentration included"""
#         dispense_form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type IV, you should enter concentration',
#             dispense_form.errors.get('concentration', []))
# 
#     def test_without_number_of_tablets(self):
#         """Test when DISPENSE TYPE:IV is chosen with number of tablets not included"""
#         dispense_form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type IV, you should NOT enter number of tablets',
#             dispense_form.errors.get('number_of_tablets', []))
# 
#     def test_without_total_number_of_tablets(self):
#         """Test when DISPENSE TYPE:IV is chosen with total number of tablets included"""
#         dispense_form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type IV, you should NOT enter total number of tablets',
#             dispense_form.errors.get('total_number_of_tablets', []))
# 
#     def test_with_dose(self):
#         """Test when DISPENSE TYPE:IV is chosen with syrup dose included"""
#         self.data['dose'] = '5mL'
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn(
#             'You have selected dispense type IV, you should NOT enter dose',
#             dispense_form.errors.get('dose', []))
# 
#     def test_without_dose(self):
#         """Test when DISPENSE TYPE:IV is chosen with syrup dose not included"""
#         dispense_form = DispenseForm(data=self.data)
#         self.assertNotIn(
#             'You have selected dispense type IV, you should NOT enter dose',
#             dispense_form.errors.get('dose', []))
