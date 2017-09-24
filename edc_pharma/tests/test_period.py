from datetime import datetime, date
from django.test import TestCase, tag

from ..classes import Period


@tag('period')
class TestPeriod(TestCase):

    @tag('period.1')
    def test_of_days(self):
        period = Period(timepoint=datetime(2017, 9, 25))
        period.of_days(days=1)
        self.assertEqual(period.start_date.date(), date(2017, 9, 25))
        self.assertEqual(period.end_date.date(), date(2017, 9, 25))

    def test_of_days1(self):
        period = Period(timepoint=datetime(2017, 8, 24))
        period.of_days(days=2)
        self.assertEqual(period.start_date.date(), datetime(2017, 8, 24).date())
        self.assertEqual(period.end_date.date(), datetime(2017, 8, 25).date())

    def test_of_months(self):
        period = Period(timepoint=datetime(2017, 8, 24))
        period.of_months(months=1)
        self.assertEqual(period.start_date.date(), datetime(2017, 8, 24).date())
        self.assertEqual(period.end_date.date(), datetime(2017, 9, 25).date())

    def test_of_weeks(self):
        period = Period(timepoint=datetime(2017, 8, 24))
        period.of_weeks(weeks=1)
        self.assertEqual(period.start_date.date(), datetime(2017, 8, 24).date())
        self.assertEqual(period.end_date.date(), datetime(2017, 8, 31).date())

    def test_of_weeks1(self):
        period = Period(timepoint=datetime(2017, 8, 24))
        period.of_months(months=1)
        self.assertEqual(period.start_date.date(), datetime(2017, 8, 24).date())
        self.assertEqual(period.end_date.date(), datetime(2017, 9, 25).date())
