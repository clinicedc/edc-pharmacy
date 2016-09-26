from django.utils import timezone
from datetime import datetime, date
from django.test import TestCase
from django.db import IntegrityError

from edc_constants.constants import YES, NO, NOT_APPLICABLE, UNKNOWN
from edc_pharma.models import TABLET, SYRUP, IV
from edc_base.model.validators.date import date_not_future
from edc_constants.choices import GENDER

from edc_pharma.forms import DispenseForm
from django import forms
from edc_pharma.models import Dispense, Protocol, Site, Patient, Medication
from edc_pharma.tests.factories.patient_factory import PatientFactory


class TestDispense(TestCase):
    
    def setUp(self):
        self.protocol = Protocol.objects.create(number='BHP001', name='001')
        self.site = Site.objects.create(protocol=self.protocol, site_code='35', telephone_number='3914503')
        self.patient = Patient.objects.create(
            subject_identifier='123',
            initials='KAB',
            gender='MALE',
            dob='1990-12-01',
            sid='123',
            site=self.site,
            consent_datetime=datetime(2005, 7, 14, 12, 30))
        self.medication = Medication.objects.create(
            name='compral',
            protocol=self.protocol,
            storage_instructions='store at 5 deg centigrade')

    def test_valid_form(self):
        data = {
            'patient': self.patient,
            'medication': self.medication,
            'dispense_type': 'IV',
            'number_of_tablets': 1,
            'times_per_day': 3,
            'total_number_of_tablets': 30,
            'prepared_datetime': datetime(2005, 7, 14, 12, 30),
            'prepared_date': date(2005, 7, 14), }
        form = DispenseForm(data=data)
        self.assertTrue(form.is_valid)

#     def test_invalid_form(self):
#         data = {
#             'patient': self.patient,
#             'medication': self.medication,
#             'dispense_type': 'IV',
#             'number_of_tablets': 1,
#             'times_per_day': 3,
#             'total_number_of_tablets': 30,
#             'prepared_datetime': datetime(2005, 7, 14, 12, 30),
#             'prepared_date': date(2005, 7, 14), }
#         form = DispenseForm(data=data)
#         self.assertFalse(form.is_valid)
# 
#     dispense_form = DispenseForm
# 
#     def setUp(self):
#         super(TestDispense, self).setUp()
#         self.patient = PatientFactory()
#         self.data = {
#             'prepared_datetime': timezone.now(),
#             'dispense_type': TABLET,
# #             'tablet': YES,
# #             'syrup': YES,
# #             'iv': YES,
#             'number_of_tablets': 1,
#             'syrup_volume': '50',
#             'total_dosage_volume': '100',
#             'total_number_of_tablets': 50,
#             'times_per_day': 3,
#             'iv_duration': '10',
#             'iv_concentration': '5',
#         }

#     def test_valid_dispense_form(self):
#         dispense = Dispense(**self.data)
#         dispense_form = DispenseForm(data=self.data)
#         self.assertTrue(dispense_form.is_valid())

#     def test_validate_taking_not_syrup(self):
#             """Test if the patient is not taking syrup"""
#             self.data['tablet'] = YES
#             self.data['syrup_volume'] = 0
#             dispense_form = DispenseForm(data=self.data)
#             self.assertIn('You have selected dispense type tablet, you should NOT enter syrup volume',
#                           dispense_form.errors.get('__all__'))
      
#     def test_validate_taking_right_amount_tablets(self):
#         """Test if the patient is taking correct amount of tablets"""
#         self.data['tablet'] = YES
#         self.data['number_of_tablets'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should enter correct number of tablet to take.',
#                       dispense_form.errors.get('__all__'))
#    
#     def test_validate_taking_tablet_at_right_time(self):
#         """Test if the patient is taking tablets at right time"""
#         self.data['tablet'] = YES
#         self.data['times_per_day'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should enter correct prescription ',
#                       dispense_form.errors.get('__all__'))
#    
#     def test_validate_taking_right_amount_of_tablet_from_pharmacist(self):
#         """Test if the patient is taking tablets at right time"""
#         self.data['tablet'] = YES
#         self.data['total_number_of_tablets'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should NOT enter tablet total',
#                       dispense_form.errors.get('__all__'))
#    
#     def test_validate_taking_tablet_package_is_full(self):
#         """Test if the patient is taking correct dosage volume for syrup"""
#         self.data['tablet'] = YES
#         self.data['total_dosage_volume'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should NOT enter syrup dosage volume',
#                       dispense_form.errors.get('__all__'))
#  
#     def test_validate_taking_iv(self):
#         """Test if the patient is not taking iv within set time(minutes)"""
#         self.data['tablet'] = YES
#         self.data['iv'] = NO
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should select dispense type iv',
#                       dispense_form.errors.get('__all__'))
#  
#     def test_validate_iv_concentration(self):
#         """Test if the patient is not taking iv in a certain volume(per ml)"""
#         self.data['tablet'] = YES
#         self.data['iv_concentration'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should NOT enter iv concentration',
#                       dispense_form.errors.get('__all__'))
# 
#     def test_validate_taking_syrup(self):
#         """Test if the patient is not taking syrup"""
#         self.data['syrup'] = YES
#         self.data['syrup_volume'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type syrup, you should enter syrup volume',
#                       dispense_form.errors.get('__all__'))
#  
#     def test_validate_taking_right_dosage_volume(self):
#         """Test if the patient is taking correct amount of tablets"""
#         self.data['syrup'] = YES
#         self.data['total_dosage_volume'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type syrup, you should enter correct volume .',
#                       dispense_form.errors.get('__all__'))
   
#     def test_validate_taking_tablet_at_right_time(self):
#         """Test if the patient is taking tablets at right time"""
#         self.data['tablet'] = YES
#         self.data['times_per_day'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should enter correct prescription ',
#                       dispense_form.errors.get('__all__'))
#    
#     def test_validate_taking_right_amount_of_tablet_from_pharmacist(self):
#         """Test if the patient is taking tablets at right time"""
#         self.data['tablet'] = YES
#         self.data['total_number_of_tablets'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should NOT enter tablet total',
#                       dispense_form.errors.get('__all__'))
#    
#     def test_validate_taking_tablet_package_is_full(self):
#         """Test if the patient is taking correct dosage volume for syrup"""
#         self.data['tablet'] = YES
#         self.data['total_dosage_volume'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should NOT enter syrup dosage volume',
#                       dispense_form.errors.get('__all__'))
#  
#     def test_validate_taking_iv(self):
#         """Test if the patient is not taking iv within set time(minutes)"""
#         self.data['tablet'] = YES
#         self.data['iv'] = NO
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should select dispense type iv',
#                       dispense_form.errors.get('__all__'))
#  
#     def test_validate_iv_concentration(self):
#         """Test if the patient is not taking iv in a certain volume(per ml)"""
#         self.data['tablet'] = YES
#         self.data['iv_concentration'] = 0
#         dispense_form = DispenseForm(data=self.data)
#         self.assertIn('You have selected dispense type tablet, you should NOT enter iv concentration',
#                       dispense_form.errors.get('__all__'))

