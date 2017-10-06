from datetime import datetime, date
from edc_pharma.scheduler.dispense_plan_scheduler import DispensePlanSchedulerException

from django.test import tag, TestCase

from ..constants import WEEKS
from ..models import DispenseSchedule, DispenseTimepoint
from ..print_profile import site_profiles
from ..scheduler import DispensePlanScheduler, InvalidSchedulePlanConfig


class RandomizedSubjectDummy:

    def __init__(self, randomization_datetime=None, subject_identifier=None):
        self.randomization_datetime = randomization_datetime or datetime.today()
        self.subject_identifier = subject_identifier


@tag('dispense_scheduler')
class TestDispensePlanScheduler(TestCase):

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

    def test_schedule_subject(self):
        """Assert that calculated subject_schedules equals
        number of specified in a plan."""
        randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            randomized_subject=randomized_subject, dispense_plan=self.dispense_plan)
        self.assertEqual(len(dispense.subject_schedules),
                         len(self.dispense_plan))

    @tag('dispense_scheduler.1')
    def test_schedule_subject1(self):
        """Assert that calculated subject_schedules equals
        number of specified in a plan."""
        del self.dispense_plan['schedule2']
        randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            randomized_subject=randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control_arm')
        self.assertEqual(len(dispense.subject_schedules), 1)

    def test_schedule_subject_invalid_plan(self):
        """Assert that calculated subject_schedules equals
        number of specified in a plan."""
        invalid_dispense_plan = {
            'schedule1': {
                'number_of_visits': 2, 'duration': 2}
        }
        randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')

        dispense_scheduler = DispensePlanScheduler(
            randomized_subject=randomized_subject,
            dispense_plan=invalid_dispense_plan,
            arm='control_arm')

        self.assertRaises(
            InvalidSchedulePlanConfig,
            dispense_scheduler.validate_dispense_plan,
            dispense_plan=invalid_dispense_plan)

    def test_last_schedule(self):
        """Assert that last schedule dates are calculated correctly."""
        randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24), subject_identifier='1111')
        scheduller = DispensePlanScheduler(
            randomized_subject=randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control_arm')
        last_schedule = scheduller.subject_schedules.last()
        self.assertEqual(
            last_schedule.period.start_date.date(), date(2017, 9, 8))
        self.assertEqual(
            last_schedule.period.end_date.date(), date(2017, 11, 3))

    def test_schedule_subject2(self):
        """Assert that all schedules are created successfully."""
        randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24), subject_identifier='1111')
        dispense = DispensePlanScheduler(
            randomized_subject=randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control_arm')
        dispense.create_schedules()
        self.assertEqual(DispenseSchedule.objects.all().count(), 2)

    def test_schedule_subject3(self):
        randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            randomized_subject=randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control_arm')
        dispense.create_schedules()
        schedule = DispenseSchedule.objects.all().first()
        self.assertEqual(
            DispenseTimepoint.objects.filter(schedule=schedule).count(), 2)

    def test_schedule_subject4(self):
        randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            randomized_subject=randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control_arm')
        dispense.create_schedules()
        self.assertEqual(DispenseTimepoint.objects.all().count(), 4)

    @tag('test_schedule_subject6')
    def test_schedule_subject6(self):
        for i in range(1, 5):
            randomized_subject = RandomizedSubjectDummy(
                randomization_datetime=datetime(2017, 8, 24),
                subject_identifier=f'111{i}')
            dispense = DispensePlanScheduler(
                randomized_subject=randomized_subject,
                dispense_plan=self.dispense_plan,
                arm='control_arm')
            dispense.create_schedules()
            self.assertEqual(DispenseTimepoint.objects.all().count(), 4 * i)

    @tag('test_schedule_subject7')
    def test_schedule_subject7(self):
        for i in range(1, 5):
            randomized_subject = RandomizedSubjectDummy(
                randomization_datetime=datetime(2017, 8, 24),
                subject_identifier=f'111{i}')
            self.assertRaises(DispensePlanSchedulerException,
                              DispensePlanScheduler,
                              randomized_subject=randomized_subject,
                              arm='control_arm_wrong')

    @tag('schedule_subject5')
    def test_schedule_subject5(self):
        randomized_subject = RandomizedSubjectDummy(
            randomization_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            randomized_subject=randomized_subject,
            dispense_plan=self.dispense_plan,
            arm='control_arm')
        dispense.create_schedules()
        schedule = DispenseSchedule.objects.all().order_by(
            'created').first()
        p1, p2 = DispenseTimepoint.objects.filter(schedule=schedule)
        self.assertEqual(p1.timepoint, date(2017, 8, 24))
        self.assertEqual(p2.timepoint, date(2017, 9, 1))
