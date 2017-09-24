from django.test import tag, TestCase

from datetime import datetime

from ..classes import DispensePlanScheduler
from ..models import DispenseSchedule, DispenseryPlan


class RandomizedSubjectDummy:

    def __init__(self, report_datetime=None, subject_identifier=None):
        self.report_datetime = report_datetime or datetime.today()
        self.subject_identifier = subject_identifier


@tag('dispense_scheduler')
class TestDispensePlanScheduler(TestCase):

    def test_schudule_subject(self):
        randomized_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=randomized_subject)
        self.assertEqual(len(dispense.subject_schedules), 2)

    def test_schudule_subject1(self):
        randomized_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=randomized_subject)
        last_schedule = dispense.subject_schedules.last()
        self.assertEqual(
            last_schedule.period.start_date.date(),
            datetime(2017, 9, 8).date())
        self.assertEqual(
            last_schedule.period.end_date.date(),
            datetime(2017, 11, 3).date())

    def test_schudule_subject2(self):
        randomized_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=randomized_subject)
        dispense.prepare()
        self.assertEqual(DispenseSchedule.objects.all().count(), 2)

    def test_schudule_subject3(self):
        randomized_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=randomized_subject)
        dispense.prepare()
        schedule = DispenseSchedule.objects.all().first()
        self.assertEqual(
            DispenseryPlan.objects.filter(schedule=schedule).count(), 2)

    def test_schudule_subject4(self):
        randomized_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=randomized_subject)
        dispense.prepare()
        self.assertEqual(DispenseryPlan.objects.all().count(), 4)

    def test_schudule_subject5(self):
        randomized_subject = RandomizedSubjectDummy(
            report_datetime=datetime(2017, 8, 24),
            subject_identifier='1111')
        dispense = DispensePlanScheduler(
            enrolled_subject=randomized_subject)
        dispense.prepare()
        schedule = DispenseSchedule.objects.all().first()
        p1, p2 = DispenseryPlan.objects.filter(schedule=schedule)
        self.assertEqual(p1.timepoint, datetime(2017, 8, 24).date())
        self.assertEqual(p2.timepoint, datetime(2017, 9, 1).date())
