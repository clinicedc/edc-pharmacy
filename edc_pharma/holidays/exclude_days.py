from ..utils import is_weekend_day
from .country_holidays import CountryHolidays
from .move_day import MoveDay


class ExcludeDays:
    """Given a date it will change date to next/previous day if date is holiday
    or weekend.
    """

    holiday_cls = CountryHolidays
    move_day_cls = MoveDay

    def __init__(self, day=None, *args, **kwargs):
        self.day = day
        self.is_holiday = self.holiday_cls().is_holiday(day=day)
        self.is_weekend_day = is_weekend_day(day=day)
        self.exclude()

    def __repr__(self):
        return f'{self.day}'

    def custom_days(self):
        return []

    def exclude(self):
        while self.holiday_cls().is_holiday(day=self.day):
            next_day = self.move_day_cls(
                day=self.day, forward=True).next_day()
            self.day = next_day
        while is_weekend_day(day=self.day):
            next_day = self.move_day_cls(
                day=self.day, forward=True).next_day()
            self.day = next_day
