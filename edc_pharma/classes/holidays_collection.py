import holidays

from datetime import date
from collections import OrderedDict


class BaseHoliday:

    def common(self, year):
        self[date(year, 12, 25)] = "Christmas Day"
        self[date(year, 12, 26)] = "Boxing Day"
        self[date(year, 1, 1)] = "New Year"


class Botswana(BaseHoliday, holidays.HolidayBase):
    def _populate(self, year):
        super(Botswana, self).common(year)
        self[date(year, 1, 2)] = "Public Holiday"
        self[date(year, 4, 14)] = "Good Friday"
        self[date(year, 4, 15)] = "Public Holiday"
        self[date(year, 4, 17)] = "Easter Monday"
        self[date(year, 5, 1)] = "May Day/Labour Day"
        self[date(year, 5, 25)] = "Ascension Day"
        self[date(year, 7, 1)] = "Sir Seretse Khama Day"
        self[date(year, 7, 17)] = "President's Day"
        self[date(year, 7, 18)] = "Public Holiday"
        self[date(year, 9, 30)] = "Botswana Day"
        self[date(year, 10, 2)] = "Public Holiday"


class BW(Botswana):
    pass


class Zimbabwe(BaseHoliday, holidays.HolidayBase):
    def _populate(self, year):
        super(Zimbabwe, self).common(year)
        self[date(year, 1, 1)] = "New Year"
        self[date(year, 1, 2)] = "Public Holiday"
        self[date(year, 4, 14)] = "Good Friday"
        self[date(year, 4, 15)] = "Public Holiday"
        self[date(year, 4, 17)] = "Easter Monday"
        self[date(year, 5, 1)] = "May Day/Labour Day"
        self[date(year, 5, 25)] = "Ascension Day"
        self[date(year, 7, 1)] = "Sir Seretse Khama Day"
        self[date(year, 7, 17)] = "President's Day"
        self[date(year, 7, 18)] = "Public Holiday"
        self[date(year, 9, 30)] = "Botswana Day"
        self[date(year, 10, 2)] = "Public Holiday"
        self[date(year, 12, 25)] = "Christmas Day"
        self[date(year, 12, 26)] = "Boxing Day"


class ZIM(Zimbabwe):
    pass


class SouthAfrica(BaseHoliday, holidays.HolidayBase):
    def _populate(self, year):
        super(SouthAfrica, self).common(year)
        self[date(year, 1, 2)] = "Public Holiday"
        self[date(year, 4, 14)] = "Good Friday"
        self[date(year, 4, 15)] = "Public Holiday"
        self[date(year, 4, 17)] = "Easter Monday"
        self[date(year, 5, 1)] = "May Day/Labour Day"
        self[date(year, 5, 25)] = "Ascension Day"
        self[date(year, 7, 1)] = "Sir Seretse Khama Day"
        self[date(year, 7, 17)] = "President's Day"
        self[date(year, 7, 18)] = "Public Holiday"
        self[date(year, 9, 30)] = "Botswana Day"
        self[date(year, 10, 2)] = "Public Holiday"


class ZA(SouthAfrica):
    pass


class Uganda(BaseHoliday, holidays.HolidayBase):
    def _populate(self, year):
        super(Uganda, self).common(year)
        self[date(year, 1, 2)] = "Public Holiday"
        self[date(year, 4, 14)] = "Good Friday"
        self[date(year, 4, 15)] = "Public Holiday"
        self[date(year, 4, 17)] = "Easter Monday"
        self[date(year, 5, 1)] = "May Day/Labour Day"
        self[date(year, 5, 25)] = "Ascension Day"
        self[date(year, 7, 1)] = "Sir Seretse Khama Day"
        self[date(year, 7, 17)] = "President's Day"
        self[date(year, 7, 18)] = "Public Holiday"
        self[date(year, 9, 30)] = "Botswana Day"
        self[date(year, 10, 2)] = "Public Holiday"


class Lesotho(BaseHoliday, holidays.HolidayBase):
    def _populate(self, year):
        super(Lesotho, self).common(year)
        self[date(year, 1, 2)] = "Public Holiday"
        self[date(year, 4, 14)] = "Good Friday"
        self[date(year, 4, 15)] = "Public Holiday"
        self[date(year, 4, 17)] = "Easter Monday"
        self[date(year, 5, 1)] = "May Day/Labour Day"
        self[date(year, 5, 25)] = "Ascension Day"
        self[date(year, 7, 1)] = "Sir Seretse Khama Day"
        self[date(year, 7, 17)] = "President's Day"
        self[date(year, 7, 18)] = "Public Holiday"
        self[date(year, 9, 30)] = "Botswana Day"
        self[date(year, 10, 2)] = "Public Holiday"


holidays_collection = OrderedDict()
holidays_collection.update({
    'botswana': Botswana(),
    'zimbabwe': Zimbabwe(),
    'lesotho': Lesotho(),
    'uganda': Uganda(),
    'southafrica': SouthAfrica()})
