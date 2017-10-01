from datetime import datetime
from edc_pharma.constants import MONTHS

from django.test import TestCase, tag

from ..classes import DispensePlanScheduleOverlapError
from ..constants import WEEKS
from ..scheduler import Schedule, ScheduleCollection
from ..scheduler.period import Period


dispense_plan = {
    'schedule1': {
        'number_of_visits': 2,
        'duration': 2,
        'unit': WEEKS,
    },
    'schedule2': {
        'number_of_visits': 2,
        'duration': 8,
        'unit': WEEKS
    }
}


@tag('dispense_schedule')
class TestDispenseSchedule(TestCase):

    def test_repr(self):
        period = Period(
            timepoint=datetime(2017, 8, 24),
            unit=WEEKS,
            duration=2)
        schedule = Schedule(period, name='schedule1')
        self.assertIsNotNone(schedule.__repr__())

    @tag('schedule.1')
    def test_schedule_with_visit(self):
        period = Period(
            timepoint=datetime(2017, 8, 24), unit=WEEKS, duration=2)
        schedule = Schedule(
            period, name='schedule1', number_of_visits=1)
        self.assertEqual(
            schedule.visits.get('visit0').timepoint_datetime.date(),
            datetime(2017, 8, 24).date())

    def test_schedule_with_visit1(self):
        period = Period(
            timepoint=datetime(2017, 8, 24), unit=WEEKS, duration=2)
        schedule = Schedule(
            name='schedule1', number_of_visits=2, period=period)
        self.assertEqual(
            schedule.visits.get('visit0').timepoint_datetime.date(),
            datetime(2017, 8, 24).date())
        self.assertEqual(
            schedule.visits.get('visit1').timepoint_datetime.date(),
            datetime(2017, 9, 1).date())

    def test_schedule_with_visit3(self):
        period = Period(
            timepoint=datetime(2017, 8, 24),
            unit=WEEKS,
            duration=2)
        schedule = Schedule(
            name='schedule1',
            number_of_visits=2,
            period=period)
        self.assertEqual(len(schedule.visits), 2)

    @tag('schedule.1')
    def test_schedule_with_visit2(self):
        period = Period(
            timepoint=datetime(2017, 8, 24), unit=WEEKS, duration=8)
        schedule = Schedule(
            name='schedule1', number_of_visits=2, period=period)
        self.assertEqual(
            schedule.visits.get('visit0').timepoint_datetime.date(),
            datetime(2017, 8, 24).date())
        self.assertEqual(
            schedule.visits.get('visit1').timepoint_datetime.date(),
            datetime(2017, 9, 22).date())

    @tag('schedule.1')
    def test_add_schedule(self):
        period = Period(
            timepoint=datetime(2017, 8, 24), unit=WEEKS, duration=8)
        schedule = Schedule(
            name='schedule1',
            number_of_visits=2,
            period=period)
        schedules = ScheduleCollection(schedule=schedule)
        self.assertTrue(len(schedules), 1)

    @tag('schedule.1')
    def test_add_schedule1(self):
        schedules = ScheduleCollection()
        p = Period(
            timepoint=datetime(2017, 8, 24), unit=WEEKS, duration=2)
        schedule = Schedule(name='schedule1', number_of_visits=1, period=p)
        schedules.add(schedule=schedule)
        self.assertEqual(len(schedules), 1)

        p2 = Period(timepoint=datetime(2017, 9, 6), unit=WEEKS, duration=2)
        schedule2 = Schedule(
            name='schedule2', number_of_visits=2, period=p2)
        self.assertRaises(
            DispensePlanScheduleOverlapError, schedules.add,
            schedule=schedule2)

    def test_get_last_schedule(self):
        schedules = ScheduleCollection()
        enrollment_plan = dispense_plan.get('schedule1')
        period = Period(
            timepoint=datetime(2017, 8, 24),
            duration=enrollment_plan.get('duration'),
            unit=enrollment_plan.get('unit'))
        schedule = Schedule(
            name='schedule1',
            number_of_visits=enrollment_plan.get('number_of_visits'),
            period=period)
        schedules.add(schedule=schedule)

        followup_plan = dispense_plan.get('schedule2')
        p2 = Period(
            timepoint=schedules.next_timepoint,
            duration=followup_plan.get('duration'),
            unit=followup_plan.get('unit'))
        schedule2 = Schedule(
            name='schedule2',
            number_of_visits=followup_plan.get('number_of_visits'), period=p2)
        schedules.add(schedule=schedule2)
        self.assertTrue(schedule2.name, schedules.last().name)

    def test_next_schedule_timepoint(self):
        schedules = ScheduleCollection()
        enrollment_plan = dispense_plan.get('schedule1')
        p = Period(
            timepoint=datetime(2017, 8, 24),
            duration=enrollment_plan.get('duration'),
            unit=enrollment_plan.get('unit'))
        schedule = Schedule(
            name='schedule1',
            number_of_visits=enrollment_plan.get('number_of_visits'),
            period=p)
        schedules.add(schedule=schedule)
        self.assertEqual(schedules.next_timepoint, datetime(2017, 9, 8))

    def test_schedule_with_visit_selector(self):
        period = Period(
            timepoint=datetime(2017, 8, 24),
            duration=2, unit=WEEKS)
        schedule = Schedule(
            name='schedule1',
            number_of_visits=1,
            period=period)
        self.assertEqual(len(schedule.selector.selected_timepoints), 1)

    def test_schedule_with_visit_selector1(self):
        period = Period(
            timepoint=datetime(2017, 8, 24),
            duration=2, unit=WEEKS)
        schedule = Schedule(
            name='schedule1',
            number_of_visits=2,
            period=period)
        self.assertEqual(len(schedule.selector.selected_timepoints), 2)

    def test_schedule_with_visit_selector2(self):
        period = Period(
            timepoint=datetime(2017, 8, 24), duration=2, unit=WEEKS)
        schedule = Schedule(
            name='schedule1',
            number_of_visits=2,
            period=period)
        first_day, next_timepoint = schedule.selector.selected_timepoints
        self.assertEqual(first_day.date(), datetime(2017, 8, 24).date())
        self.assertEqual(next_timepoint.date(), datetime(2017, 9, 1).date())

    @tag('selector')
    def test_schedule_with_visit_selector3(self):
        period = Period(
            timepoint=datetime(2017, 8, 24), unit=WEEKS, duration=2)
        schedule = Schedule(
            name='schedule1',
            number_of_visits=3,
            period=period)
        first_day, next_timepoint, third_timepoint = (
            schedule.selector.selected_timepoints)
        self.assertEqual(first_day.date(), datetime(2017, 8, 24).date())
        self.assertEqual(next_timepoint.date(), datetime(2017, 8, 29).date())
        self.assertEqual(third_timepoint.date(), datetime(2017, 9, 1).date())

    def test_schedule_with_visit_selector4(self):
        period = Period(
            timepoint=datetime(2017, 8, 24), unit=MONTHS, duration=2)
        schedule = Schedule(
            name='schedule1', number_of_visits=2, period=period)
        first_day, next_timepoint = (
            schedule.selector.selected_timepoints)
        self.assertEqual(first_day.date(), datetime(2017, 8, 24).date())
        self.assertEqual(next_timepoint.date(), datetime(2017, 9, 25).date())

    def test_schedule_with_visit_selector5(self):
        period = Period(
            timepoint=datetime(2017, 8, 24),
            unit=WEEKS, duration=8)
        schedule = Schedule(
            name='schedule1',
            number_of_visits=2, period=period)
        first_day, next_timepoint = (
            schedule.selector.selected_timepoints)
        self.assertEqual(first_day.date(), datetime(2017, 8, 24).date())
        self.assertEqual(next_timepoint.date(), datetime(2017, 9, 22).date())
