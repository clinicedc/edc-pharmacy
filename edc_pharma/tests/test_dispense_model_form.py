# import pytz
# 
# from datetime import datetime, time, date
# from dateutil.relativedelta import relativedelta
# 
# from django.test import TestCase
# from django.utils import timezone
# 
# from ..choices import TABLET
# from ..forms import DispenseForm
# 
# from .factories import SiteFactory, PatientFactory, ProtocolFactory, MedicationFactory, DispenseFactory
# 
# 
# class TestDispenseModel(TestCase):
#     """Setup data with all required fields for DISPENSE TYPE: IV"""
#     def setUp(self):
#         self.protocol = ProtocolFactory()
#         self.site = SiteFactory()
#         self.patient = PatientFactory()
#         self.medication = MedicationFactory()
#         self.dispense = DispenseFactory(patient=self.patient, medication=self.medication)
#         now = timezone.make_aware(datetime.combine(timezone.now(), time(0, 0, 0)), timezone=pytz.timezone('UTC'))
#         self.data = {
#             'patient': self.patient.id,
#             'medication': self.medication.id,
#             'dispense_type': TABLET,
#             'number_of_tablets': 1,
#             'total_number_of_tablets': 30,
#             'dose': None,
#             'total_volume': None,
#             'duration': None,
#             'times_per_day': 1,
#             'concentration': None,
#             'prepared_date': now,
#             'weight': None,
#             'prepared_datetime': timezone.now()}
# 
#     def test_refill_date_logic(self):
#         """Test to verify whether the refill date method returns the right date"""
#         self.assertEqual(self.dispense.refill_datetime, timezone.now() + relativedelta(days=16))
# 
#     def test_unique_date_medication_patient(self):
#         """Test to verify that unique integrity in fields: patient, medication, prepared_date is maintained"""
#         form = DispenseForm(data=self.data)
#         self.assertFalse(form.is_valid())
