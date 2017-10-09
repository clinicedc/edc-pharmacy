from datetime import datetime

from django.test import TestCase

from ..holidays import Country


class TestCountry(TestCase):

    def setUp(self):
        self.country = Country()

    def test_exclude_day(self):
        workday = self.country.move_to_workday(datetime(2017, 9, 30))
        self.assertNotEqual(
            workday.day.date(), datetime(2017, 9, 30).date())

    def test_exclude_day1(self):
        workday = self.country.move_to_workday(datetime(2017, 9, 30))
        self.assertEqual(
            workday.day.date(), datetime(2017, 10, 2).date())
