from datetime import datetime, date
from edc_pharma.models.dispense_schedule import DispenseSchedule

from django.test import tag, TestCase

from ..classes import DispensePlanScheduler
from ..constants import WEEKS
from ..models import DispenseTimepoint
from ..site_dispense_profiles import site_profiles


class RandomizedSubjectDummy:

    def __init__(self, randomization_datetime=None, subject_identifier=None):
        self.randomization_datetime = randomization_datetime or datetime.today()
        self.subject_identifier = subject_identifier


@tag('getter')
class TestDispenseTimepointGetter(TestCase):

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

    def test_schedule_subject_next(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        dispense_next = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created')[1]
        self.assertNotEqual(dispense_timepoint.timepoint,
                            dispense_next.timepoint)
        self.assertEqual(dispense_timepoint.next().timepoint,
                         dispense_next.timepoint)

    def test_schedule_subject_previous(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier
        ).order_by('created').first()
        dispense_current = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier
        ).order_by('created')[1]
        self.assertEqual(dispense_current.previous().timepoint,
                         dispense_timepoint.timepoint)

    def test_schedule_subject_completed(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier
        ).order_by('created').first()
        dispense_timepoint.is_dispensed = True
        dispense_timepoint.save()
        self.assertEqual(dispense_timepoint.completed().count(), 1)

    def test_schedule_subject_next_timepoints(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier
        ).order_by('created').first()
        dispense_timepoint.is_dispensed = True
        dispense_timepoint.save()
        self.assertGreater(dispense_timepoint.next_timepoints().count(), 0)

    @tag('getter.current')
    def test_dispense_schedule_current(self):
        dispense_schedule = DispenseSchedule.objects.filter(
            subject_identifier=self.enrolled_subject.subject_identifier,
        ).order_by('created').first()
        self.assertEqual(dispense_schedule.name, 'schedule1')
        self.assertEqual(dispense_schedule.sequence, 1)
        self.assertEqual(dispense_schedule.start_date, date(2017, 8, 24))

    @tag('getter.current')
    def test_dispense_schedule_next(self):
        dispense_schedule = DispenseSchedule.objects.filter(
            subject_identifier=self.enrolled_subject.subject_identifier,
        ).order_by('created').first()
        schedule = dispense_schedule.next()
        self.assertEqual(schedule.name, 'schedule2')
        self.assertEqual(schedule.sequence, 2)

    @tag('getter.current')
    def test_dispense_schedule_previous(self):
        dispense_schedule = DispenseSchedule.objects.filter(
            subject_identifier=self.enrolled_subject.subject_identifier,
        ).order_by('created').first()
        next_schedule = dispense_schedule.next()
        previous_schedule = next_schedule.previous()
        self.assertEqual(previous_schedule.name, 'schedule1')
        self.assertEqual(previous_schedule.sequence, 1)

    @tag('getter.profile')
    def test_dispense_schedule_profile(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        self.assertTrue(dispense_timepoint.print_profile)

    @tag('getter.profile')
    def test_dispense_schedule_profile_medications(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        profile = dispense_timepoint.print_profile
        self.assertTrue(profile.medication_types)

    @tag('getter.profile')
    def test_dispense_profile_medications(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        self.assertTrue(dispense_timepoint.profile_medications)

    @tag('getter.profile')
    def test_schedule_description(self):
        dispense_timepoint = DispenseTimepoint.objects.filter(
            schedule__subject_identifier=self.enrolled_subject.subject_identifier,
            is_dispensed=False
        ).order_by('created').first()
        print(dispense_timepoint.schedule.description, "<<<<<<<<<<<<<<<<<")
