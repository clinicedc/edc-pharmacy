from datetime import datetime

import arrow
from django.test import TestCase, tag

from ..holidays import Country


@tag('Country')
class TestCountry(TestCase):

    def setUp(self):
        self.country = Country()

    def test_exclude_day(self):
        start_datetime = arrow.Arrow.fromdatetime(
            datetime(2017, 9, 30)).datetime
        workday = self.country.move_to_workday(start_datetime)
        print(workday)
        self.assertNotEqual(
            workday, datetime(2017, 9, 30).date())

    def test_exclude_day1(self):
        start_datetime = arrow.Arrow.fromdatetime(
            datetime(2017, 9, 30)).datetime
        expected = arrow.Arrow.fromdatetime(
            datetime(2017, 10, 2)).datetime
        workday = self.country.move_to_workday(start_datetime)
        self.assertEqual(workday, expected)
