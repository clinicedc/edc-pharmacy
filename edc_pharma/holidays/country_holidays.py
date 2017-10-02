from django.apps import apps as django_apps

from .holidays_collection import holidays_collection


class CountryHolidays:
    """Returns holidays for given country.
    """

    def __init__(self, country=None):
        self.country = country

    def is_holiday(self, day=None):
        if day in self.holiday_days:
            return True
        return False

    @property
    def holiday_days(self):
        app = django_apps.get_app_config('edc_pharma')
        self.country = self.country or app.country
        return holidays_collection.get(self.country)
