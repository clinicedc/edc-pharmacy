from datetime import datetime

from django.test import tag, TestCase

from ..constants import WEEKS
from ..models import DispenseAppointment
from ..print_profile import site_profiles
from ..scheduler import DispensePlanScheduler
from ..timepoint_descriptor import TimepointDescriptor


class RandomizedSubjectDummy:

    def __init__(self, randomization_datetime=None, subject_identifier=None):
        self.randomization_datetime = randomization_datetime or datetime.today()
        self.subject_identifier = subject_identifier


@tag('descriptor')
class TestTimepointDescriptor(TestCase):

    def setUp(self):
        self.dispense_plan = {
            'schedule1': {
                'number_of_visits': 2, 'duration': 2, 'unit': WEEKS,
                'description': 'Enrollment',
                'dispense_profile': {
                    'enrollment': site_profiles.get(name='enrollment.control'),
                    'followup': site_profiles.get(name='followup.control'),
                }},
            'schedule2': {
                'number_of_visits': 2, 'duration': 8, 'unit': WEEKS,
                'description': 'Followup',
                'dispense_profile': {
                    'enrollment': site_profiles.get(name='enrollment.control'),
                    'followup': site_profiles.get(name='followup.control'),
                }}}
        self.randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            randomized_subject=self.randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control_arm')
        dispense.create_schedules()

    def test_dispense_timepoint_start_day(self):
        dispense_timepoint = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        descriptor = TimepointDescriptor(
            dispense_timepoint=dispense_timepoint)
        self.assertTrue(descriptor.human_readiable())
        self.assertEqual('Day 1', descriptor.start_day)

    def test_dispense_timepoint_human_readiable_days_7(self):
        dispense_timepoint = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        dispense_timepoint = dispense_timepoint.next()
        descriptor = TimepointDescriptor(
            dispense_timepoint=dispense_timepoint)
        self.assertTrue(descriptor.human_readiable())
        self.assertIn('Day 8', descriptor.start_day)
        self.assertEqual('Day 14', descriptor.end_day)

    def test_dispense_timepoint_human_readiable_days_3(self):
        dispense_timepoint = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        descriptor = TimepointDescriptor(
            dispense_timepoint=dispense_timepoint)
        self.assertTrue(descriptor.human_readiable())
        self.assertEqual('Day 1', descriptor.start_day)
        self.assertEqual('Day 7', descriptor.end_day)

    def test_dispense_timepoint_human_readiable_days(self):
        dispense_timepoint = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        descriptor = TimepointDescriptor(
            dispense_timepoint=dispense_timepoint)
        self.assertTrue(descriptor.human_readiable())
        self.assertIn('Day 1', descriptor.human_readiable())
        self.assertIn('Day 7', descriptor.human_readiable())

    def test_dispense_timepoint_human_readiable_days_1(self):
        dispense_timepoint = DispenseAppointment.objects.filter(
            schedule__subject_identifier=self.randomized_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        dispense_timepoint = dispense_timepoint.next()
        descriptor = TimepointDescriptor(
            dispense_timepoint=dispense_timepoint)
        self.assertTrue(descriptor.human_readiable())
        self.assertIn('Day 8', descriptor.human_readiable())
        self.assertIn('Day 14', descriptor.human_readiable())
