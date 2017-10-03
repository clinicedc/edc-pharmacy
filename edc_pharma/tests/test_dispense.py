from datetime import datetime, date
from edc_pharma.models.dispense_history import DispenseHistory
from edc_pharma.models.dispense_timepoint import DispenseTimepoint

from django.test import tag, TestCase

from ..constants import WEEKS
from ..dispense import Dispense
from ..print_profile import site_profiles
from ..scheduler import DispensePlanScheduler


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
                    'enrollment': site_profiles.get(name='enrollment.control_arm'),
                    'followup': site_profiles.get(name='followup.control_arm'),
                }},
            'schedule2': {
                'number_of_visits': 2, 'duration': 8, 'unit': WEEKS,
                'dispense_profile': {
                    'enrollment': site_profiles.get(name='enrollment.control_arm'),
                    'followup': site_profiles.get(name='followup.control_arm'),
                }}}
        self.enrolled_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=self.enrolled_subject,
            dispense_plan=self.dispense_plan,
            arm='control_arm')
        dispense.create_schedules()

    def test_print_label(self):
        dispense_timepoint = DispenseTimepoint.objects.all().order_by(
            'created').first()
        Dispense(
            subject_identifier=self.enrolled_subject.subject_identifier,
            timepoint_id=dispense_timepoint.id)
        self.assertEqual(DispenseHistory.objects.filter(
            dispense_timepoint__schedule__subject_identifier=self.enrolled_subject.subject_identifier,
            dispense_timepoint__timepoint=date(2017, 8, 24),
        ).count(), 1)
