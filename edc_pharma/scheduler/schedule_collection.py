from collections import OrderedDict
from edc_pharma.scheduler.timepoint_selector import TimepointSelector

from dateutil.relativedelta import relativedelta


class DispensePlanScheduleOverlapError(Exception):
    pass


class Visit:
    """A class that represents a "visit" of schedule.

    Is contained by a "schedule".
    """

    def __init__(
            self, code=None, title=None, timepoint_datetime=None,
            is_scheduled=None,
            ** kwargs):
        self.code = code
        self.title = title or f'Visit {code}'
        self.timepoint_datetime = timepoint_datetime
        self.is_scheduled = is_scheduled

    def __repr__(self):
        return f'Visit({self.code}, {self.title})'

    def __str__(self):
        return self.title


class Schedule:

    """A class that represents a "schedule" of medication plan.
    Is contained by a "schedules".
    """
    timepoint_selector_cls = TimepointSelector

    def __init__(self, period, name=None, number_of_visits=None,
                 description=None):
        self._visits = {}
        self.period = period
        self.name = name
        self.number_of_visits = number_of_visits or 1
        self.workdays = self.period.workdays
        self.description = description
        self.selector = self.timepoint_selector_cls(
            workdays=self.workdays,
            number_of_visits=self.number_of_visits)
        self.prepare()

    def add(self, visit=None):
        self._visits.update({visit.code: visit})

    @property
    def visits(self):
        return self._visits

    def __repr__(self):
        return f'Visit({self.name})'

    def prepare(self):
        for i, timepoint in enumerate(self.selector.selected_timepoints):
            visit = Visit(
                code=f'visit{i}', title=i,
                timepoint_datetime=timepoint)
            self.add(visit)


class SchedulesValidator:

    def __init__(self, schedules=None):
        for key in schedules:
            schedule = schedules.get(key)
            for key in schedules:
                vschedule = schedules.get(key)
                if schedule.name == vschedule.name:
                    continue
                if (schedule.period.start_datetime <= vschedule.period.end_datetime
                        <= schedule.period.end_datetime):
                    raise DispensePlanScheduleOverlapError(
                        f'Overlap between {schedule.name} '
                        f'and {vschedule.name}. Check schedule period dates.')
                if (schedule.period.start_datetime <= vschedule.period.start_datetime
                        <= schedule.period.end_datetime):
                    raise DispensePlanScheduleOverlapError(
                        f'Overlap between {schedule.name} and {vschedule.name}.'
                        f' {vschedule.name} startdate should not fall in range '
                        f'{schedule.period.start_datetime.date()} to '
                        f'{schedule.period.end_datetime.date()} )')


class ScheduleCollection(OrderedDict):
    """A class that represents a "period" of schedule.

    Is contained by a "schedule". A period is measured in days,
    weeks, and years.
    """
    validator = SchedulesValidator

    def add(self, schedule=None):
        self.update({schedule.name: schedule})
        self.validator(schedules=self)

    @property
    def next_timepoint(self):
        last_schedule = self.last()
        if self.last():
            return last_schedule.period.end_datetime + relativedelta(days=1)

    def last(self):
        try:
            key = next(reversed(self))
        except Exception:
            pass
        else:
            return self[key]

    def first(self):
        try:
            key = next(self)
        except Exception as e:
            print(e)
        else:
            return self[key]
