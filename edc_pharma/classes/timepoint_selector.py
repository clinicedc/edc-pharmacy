

class TimepointSelector:

    """Given a list of timepoints and number of desired visits, the timepoint
    selector picks timepoint datetime. e.g

    1. timepoints = [2017-9-3, 2017-9-4, 2017-9-5],
        number of visit = 1
       the selector will self.selected_timepoints = [2017-9-3].

    2. timepoints = [2017-9-3, 2017-9-4, 2017-9-5, 2017-9-6, 2017-9-4, 2017-9-7
        ], number of visit = 2
        the selector will self.selected_timepoints = [2017-9-3, 2017-9-6].

    3. timepoints = [2017-9-3, 2017-9-4, 2017-9-5, 2017-9-6],
        number of visit = 1
       the selector will self.selected_timepoints = [
       2017-9-3, 2017-9-4, 2017-9-5, 2017-9-6].
    """

    def __init__(self, timepoints=None, number_of_visits=None, *args, **kwargs):
        self.selected_timepoints = []
        self.timepoints = timepoints
        if number_of_visits == 1:
            self.selected_timepoints.append(timepoints[0])
        elif number_of_visits == 2:
            self.selected_timepoints.append(timepoints[0])
            self.selected_timepoints.append(self.mid())
        else:
            divisible = int(len(timepoints) / number_of_visits)
            for i in range(divisible):
                if i == 0:
                    self.selected_timepoints.append(timepoints[i])
                else:
                    index = divisible * i
                    self.selected_timepoints.append(timepoints[index])

    def mid(self):
        number_of_timepoints = len(self.timepoints)

        def is_odd(days=None):
            return True if not days % 2 == 0 else False
        if is_odd(number_of_timepoints):
            number_of_days = int((number_of_timepoints / 2) + 0.5)
        else:
            number_of_days = int((number_of_timepoints / 2)) + 1
        return self.timepoints[number_of_days]
