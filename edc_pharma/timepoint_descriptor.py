from dateutil.relativedelta import relativedelta


class TimepointDescriptor:

    """Given dispense timepoint,  this class returns human readiable 
    description about the dispense timepoint.

    For Example.
        Schedule(start_date=01-10-2017, end_date=03-10-2017): Day 1 - Day 3
        Schedule is divided into 2 dispense timepoint.
        1. DispenseTimepoint(timepoint=01-10-2017) returns Day 1
        2. DispenseTimepoint(timepoint=03-10-2017) returns Day 2 to Day 3
    """

    def __init__(self, dispense_timepoint=None):
        self.dispense_timepoint = dispense_timepoint

    @property
    def start_day(self):
        if not self.dispense_timepoint.previous():
            return 'Day 1'
        else:
            _, days = self.count_days(
                dispense_timepoint=self.dispense_timepoint.previous())
            next_day = days + 1
            return f'Day {next_day}'

    @property
    def end_day(self):
        if self.dispense_timepoint.previous():
            _, days = self.count_days(
                dispense_timepoint=self.dispense_timepoint.previous())
            _, current_days = self.count_days(
                dispense_timepoint=self.dispense_timepoint)
            next_day = days + 1
            end_day = next_day + current_days
            return f'Day {end_day}'
        else:
            _, current_days = self.count_days(
                dispense_timepoint=self.dispense_timepoint)
            return f'Day {current_days}'

    @property
    def end_date(self):
        end_date, _ = self.count_days(
            dispense_timepoint=self.dispense_timepoint)
        return end_date

    def human_readiable(self):
        """Returns description of dispense timepoint example.
        (2017-08-24):day 1 to (2017-08-31): day 7.
        """
        description = (f'({self.dispense_timepoint.timepoint}):'
                       f'{self.start_day} to ({self.end_date}):'
                       f'{self.end_day}')
        return description

    def count_days(self, dispense_timepoint=None):
        """Returns count of days between two dispense timepoints.
        """
        next_timepoint = None
        end_timepoint = dispense_timepoint.schedule.end_date
        if dispense_timepoint.next():
            dispense_timepoint_obj = dispense_timepoint.next()
            next_timepoint = dispense_timepoint_obj.timepoint
            end_timepoint = next_timepoint - relativedelta(days=1)
        next_timepoint = (
            next_timepoint or dispense_timepoint.schedule.end_date)
        current_timepoint = dispense_timepoint.timepoint
        return (end_timepoint, (end_timepoint - current_timepoint).days)
