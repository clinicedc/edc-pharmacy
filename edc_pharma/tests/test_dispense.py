from datetime import datetime, date
from edc_pharma.models.dispense_appointment import DispenseAppointment
from edc_pharma.models.dispense_history import DispenseHistory

from django.test import tag, TestCase

from ..constants import WEEKS
from ..dispense import Dispense
from ..print_profile import site_profiles
from ..scheduler import DispenseScheduler


class RandomizedSubjectDummy:

    def __init__(self, randomization_datetime=None, subject_identifier=None):
        self.randomization_datetime = randomization_datetime or datetime.today()
        self.subject_identifier = subject_identifier


@tag('TestDispense')
class TestDispense(TestCase):

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
        self.randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispenseScheduler(
            randomized_subject=self.randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control')
        dispense.create_schedules()

    def test_print_label(self):
        dispense_appointment = DispenseAppointment.objects.all().order_by(
            'created').first()
        Dispense(
            subject_identifier=self.randomized_subject.subject_identifier,
            timepoint_id=dispense_appointment.id)
        self.assertEqual(DispenseHistory.objects.filter(
            dispense_appointment__schedule__subject_identifier=self.randomized_subject.subject_identifier,
            dispense_appointment__appt_datetime__date=date(2017, 8, 24),
        ).count(), 1)

    def test_print_label1(self):
        dispense_appointment = DispenseAppointment.objects.all().order_by(
            'created').first()
        Dispense(
            subject_identifier=self.randomized_subject.subject_identifier,
            timepoint_id=dispense_appointment.id)
        self.assertEqual(DispenseHistory.objects.filter(
            dispense_appointment__schedule__subject_identifier=self.randomized_subject.subject_identifier,
            dispense_appointment__appt_datetime__date=date(2017, 8, 24),
        ).count(), 1)
