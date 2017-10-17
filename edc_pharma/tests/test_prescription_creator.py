from datetime import datetime

from django.test import TestCase, tag

from ..constants import WEEKS
from ..dispense.prescription_creator import PrescriptionCreator
from ..models import DispenseAppointment
from ..models import Prescription
from ..print_profile import site_profiles
from ..scheduler import DispenseScheduler


class RandomizedSubjectDummy:

    def __init__(self, randomization_datetime=None, subject_identifier=None):
        self.randomization_datetime = randomization_datetime or datetime.today()
        self.subject_identifier = subject_identifier


@tag('prescription')
class TestPrescriptionCreator(TestCase):

    def setUp(self):
        self.dispense_plan = {
            'schedule1': {
                'number_of_visits': 2, 'duration': 2, 'unit': WEEKS,
                'dispense_profile': {
                    'enrollment': site_profiles.get(name='enrollment.control'),
                    'followup': site_profiles.get(name='followup.control'),
                }},
            'schedule2': {
                'number_of_visits': 2, 'duration': 8, 'unit': WEEKS,
                'dispense_profile': {
                    'enrollment': site_profiles.get(name='enrollment.control'),
                    'followup': site_profiles.get(name='followup.control'),
                }}}
        self.options = {'weight': 40.0, 'duration': 7}
        self.randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        DispenseScheduler(
            subject_identifier=self.randomized_subject.subject_identifier,
            dispense_plan=self.dispense_plan,
            randomization_datetime=self.randomized_subject.randomization_datetime,
            arm='control')

    def test_dispense_history_creator(self):
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).first()
        PrescriptionCreator(
            dispense_appointment=dispense_appointment, options=self.options)
        self.assertEqual(Prescription.objects.filter(
            dispense_appointment=dispense_appointment).count(), 2)

    def test_dispense_history_creator_2(self):
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).first()
        PrescriptionCreator(
            dispense_appointment=dispense_appointment, options=self.options)
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=False
        )
        self.assertEqual(dispense_appointment.count(), 4)

    def test_dispense_history_creator_3(self):
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).order_by('created').first()
        PrescriptionCreator(
            dispense_appointment=dispense_appointment, options=self.options)
        dispense_appointment = dispense_appointment.next()
        PrescriptionCreator(
            dispense_appointment=dispense_appointment,
            options=self.options)
        dispense_appointment = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
        )
        self.assertEqual(Prescription.objects.filter(
            dispense_appointment=dispense_appointment).count(), 2)
        self.assertEqual(Prescription.objects.filter(
            dispense_appointment__schedule__subject_identifier=self.randomized_subject.subject_identifier
        ).count(), 4)
