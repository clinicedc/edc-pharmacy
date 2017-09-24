from datetime import datetime

from dateutil.relativedelta import relativedelta
from ..classes.exclude_days import ExcludeDays
from ..classes.period_timepoint import PeriodTimepoint
from ..classes.timepoint_selector import TimepointSelector


class Period:

    """A class that represents a "period" of schedule.

    Is contained by a "schedule". A period is measured in days,
    weeks, and years. Given a timepoint_datetime the class calculates
    start_date and end_date excluding weekends and holidays.
    """
    exclude_days_cls = ExcludeDays
    period_timepoint_cls = PeriodTimepoint
    timepoint_selector_cls = TimepointSelector

    def __init__(self, timepoint=None, days=None, months=None, weeks=None,
                 weekends=None, holidays=None, *args, **kwargs):

        self.timepoint = timepoint
        self.start_date = None
        self.end_date = None
        self.days = days
        self.months = months
        self.weeks = weeks
        self.weekends = weekends
        self.holidays = holidays
        self.estimate()
        if self.start_date and self.end_date:
            self.timepoints = self.period_timepoint_cls(
                period=self).timepoints

    def estimate(self):
        if self.days:
            self.of_days(self.days)
        if self.months:
            self.of_months(self.months)
        if self.weeks:
            self.of_weeks(self.weeks)

    def __repr__(self):
        return f'{self.start_date.date()}, {self.end_date.date()}'

    def exclude_days(self):
        self.start_date = self.exclude_days_cls(day=self.start_date).day
        self.end_date = self.exclude_days_cls(day=self.end_date).day

    def between(self, timepoint=None, end_date=None):
        self.start_date = timepoint
        self.end_date = end_date
        self.exclude_days()

    def of_days(self, days):
        self.start_date = self.timepoint or datetime.today()
        self.end_date = self.start_date + relativedelta(days=days)
        self.end_date = self.end_date - relativedelta(days=1)
        self.exclude_days()

    def of_months(self, months):
        self.start_date = self.timepoint or datetime.today()
        self.end_date = self.start_date + relativedelta(months=months)
        self.exclude_days()

    def of_weeks(self, weeks):
        self.start_date = self.timepoint or datetime.today()
        self.end_date = self.start_date + relativedelta(weeks=weeks)
        self.exclude_days()
