from django.test import TestCase
from .models import Protocol, Site, Patient, Medication
from .forms import DispenseForm
from datetime import datetime, date


class DispenseTest(TestCase):

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
