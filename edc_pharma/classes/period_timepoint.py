from dateutil.relativedelta import relativedelta
from ..classes.exclude_days import ExcludeDays


class PeriodTimepoint:
    """Based on a period(start_date, end_date) it determines how many timepoints
    within a period. e.g
    1. Period(start_date=2017-08-31 , end_date=2017-09-01)
    returns timepoints [2017-08-31, 2017-09-01]

    2. Period(start_date=2017-08-31 , end_date=2017-09-05)
    returns timepoints [2017-08-31, 2017-09-01, 2017-09-04, 2017-09-05]
    excluding weekend (2017-09-02, 2017-09-03).
    """

    exclude_days_cls = ExcludeDays

    def __init__(self, period, *args, **kwargs):
        self.period = period

    @property
    def timepoints(self):
        days = (self.period.end_date - self.period.start_date).days
        days = days + 1
        timepoints = []
        timepoints.append(self.period.start_date)
        for i in range(days):
            timepoint = self.period.start_date + relativedelta(days=i)
            if timepoint.date() == self.period.start_date.date():
                continue
            if (not self.exclude_days_cls(day=timepoint).is_holiday and
                    not self.exclude_days_cls(day=timepoint).is_weekend_day):
                timepoints.append(timepoint)
        return timepoints
