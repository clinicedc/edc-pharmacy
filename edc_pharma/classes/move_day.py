from dateutil.relativedelta import relativedelta


class MoveDayError(Exception):
    pass


class MoveDay:

    def __init__(self, day=None, forward=None, backward=None, *args, **kwargs):
        self.day = day
        self.forward = forward
        self.backward = backward
        if not self.day:
            raise MoveDayError(
                f'self.day cannot be None. Got {self.day}')
        if self.forward and self.backward:
            raise MoveDayError(
                'You cannot move a day to both previous and forward.')

        if (not self.forward and not self.backward):
            raise MoveDayError(
                'Provide whether you a day to nextday (forward=True) or '
                'yesterday (backward=True). Both cannot be None')

    def next_day(self):
        if self.forward:
            self.day = self.day + relativedelta(days=1)
        return self.day

    def previous_day(self):
        if self.backward:
            self.day = self.day - relativedelta(days=1)
