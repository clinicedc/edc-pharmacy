from django.test import TestCase, tag
from datetime import datetime

from ..classes.period import Period
from ..constants import DAYS


@tag('timepoint')
class TestPeriodTimepoint(TestCase):

    def test_period_timepoint1(self):
        period = Period(timepoint=datetime(2017, 8, 31), duration=2, unit=DAYS)
        self.assertEqual(len(period.timepoints), 2)

    def test_period_timepoint3(self):
        period = Period(timepoint=datetime(2017, 8, 31), duration=2, unit=DAYS)
        self.assertEqual(
            period.timepoints[0].date(), datetime(2017, 8, 31).date())
        self.assertEqual(
            period.timepoints[1].date(), datetime(2017, 9, 1).date())

    def test_period_timepoint4(self):
        period = Period(timepoint=datetime(2017, 8, 31), duration=3, unit=DAYS)
        self.assertEqual(
            period.timepoints[-1].date(), datetime(2017, 9, 4).date())

    def test_period_timepoint5(self):
        period = Period(timepoint=datetime(2017, 8, 31), duration=3, unit=DAYS)
        self.assertEqual(
            len(period.timepoints), 3)

    def test_period_timepoint6(self):
        period = Period(timepoint=datetime(2017, 8, 31), duration=2, unit=DAYS)
        self.assertEqual(
            len(period.timepoints), 2)
