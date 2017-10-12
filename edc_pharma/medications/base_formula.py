

class BaseFormula:

    def __init__(self, weight=None, med_weight=None, millgrams=None, duration=None):
        self.weight = weight
        self.med_weight = med_weight
        self.millgrams = millgrams
        self.duration = duration

    @property
    def total(self):
        original_value = self.duration * self.total_per_day
        new_value = int(round(original_value))
        return new_value if (
            new_value > original_value) else int(round(original_value)) + 1

    @property
    def total_per_day(self):
        return (self.weight * self.millgrams) / self.med_weight

    def __repr__(self):
        return f'{self.definition.description}'
