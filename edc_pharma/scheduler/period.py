import arrow

from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow

from ..holidays import Country


class Period:

    """A class that represents a "period" of schedule.

    Is contained by a "schedule". A period is measured in days,
    weeks, and years. Given a timepoint_datetime the class calculates
    start_date and end_date excluding weekends and holidays.
    """
    country_cls = Country

    def __init__(self, start_datetime=None, unit=None, duration=None, **kwargs):
        self.country = self.country_cls(**kwargs)
        start_datetime = start_datetime or get_utcnow()
        rdelta = relativedelta(**{unit: duration or 0})
        end_datetime = start_datetime + rdelta
        self.start_datetime = self.country.move_to_workday(
            utc_datetime=start_datetime)
        self.end_datetime = self.country.move_to_workday(
            utc_datetime=end_datetime)

        self.workdays = []
        if self.start_datetime and self.end_datetime:
            for arr in arrow.Arrow.span_range(
                    'day', self.start_datetime, self.end_datetime):
                if self.country.is_workday(arr[0].datetime):
                    self.workdays.append(arr[0].datetime)

    def __repr__(self):
        return f'{self.start_date.date()}, {self.end_date.date()}'
