from django.test import TestCase, tag

from datetime import datetime

from ..classes import is_weekend_day


@tag('TestWeekend')
class TestWeekend(TestCase):

    def test_is_weekend(self):
        self.assertFalse(is_weekend_day(day=datetime(2017, 9, 1)))

    def test_is_weekend1(self):
        self.assertTrue(is_weekend_day(day=datetime(2017, 9, 2)))
