from datetime import datetime

from django.test import TestCase

from ..classes.exclude_days import ExcludeDays


class TestExcludeDays(TestCase):

    def test_exclude_day(self):
        exclude = ExcludeDays(day=datetime(2017, 9, 30))
        self.assertNotEqual(
            exclude.day.date(), datetime(2017, 9, 30).date())

    def test_exclude_day1(self):
        exclude = ExcludeDays(day=datetime(2017, 9, 30))
        self.assertEqual(
            exclude.day.date(), datetime(2017, 10, 2).date())
