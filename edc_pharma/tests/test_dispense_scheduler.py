from django.test import tag, TestCase

from datetime import datetime, date

from ..classes import DispensePlanScheduler
from ..models import DispenseSchedule, DispenseryPlan


class RandomizedSubjectDummy:

    def __init__(self, report_datetime=None, subject_identifier=None):
        self.report_datetime = report_datetime or datetime.today()
        self.subject_identifier = subject_identifier


@tag('dispense_scheduler')
class TestDispensePlanScheduler(TestCase):

    def test_schedule_subject(self):
        """Assert that calculated subject_schedules equals
        number of specified in a plan."""
        enrolled_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=enrolled_subject)
        self.assertEqual(len(dispense.subject_schedules), 2)

    def test_last_schedule(self):
        """Assert that last schedule are calculated """
        enrolled_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24), subject_identifier='1111')
        scheduller = DispensePlanScheduler(enrolled_subject=enrolled_subject)
        last_schedule = scheduller.subject_schedules.last()

        self.assertEqual(
            last_schedule.period.start_date.date(), date(2017, 9, 8))
        self.assertEqual(
            last_schedule.period.end_date.date(), date(2017, 11, 3))

    def test_schedule_subject2(self):
        enrolled_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=enrolled_subject)
        dispense.prepare()
        self.assertEqual(DispenseSchedule.objects.all().count(), 2)

    def test_schudule_subject3(self):
        enrolled_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=enrolled_subject)
        dispense.prepare()
        schedule = DispenseSchedule.objects.all().first()
        self.assertEqual(
            DispenseryPlan.objects.filter(schedule=schedule).count(), 2)

    def test_schedule_subject4(self):
        enrolled_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=enrolled_subject)
        dispense.prepare()
        self.assertEqual(DispenseryPlan.objects.all().count(), 4)

    def test_schedule_subject5(self):
        enrolled_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=enrolled_subject)
        dispense.prepare()
        schedule = DispenseSchedule.objects.all().first()
        p1, p2 = DispenseryPlan.objects.filter(schedule=schedule)
        self.assertEqual(p1.timepoint, datetime(2017, 8, 24).date())
        self.assertEqual(p2.timepoint, datetime(2017, 9, 1).date())
