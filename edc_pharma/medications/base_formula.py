

class BaseFormula:

    def __init__(self, weight=None, total=None, millgrams=None, duration=None):
        self.weight = weight
        self.total = total
        self.dosage = millgrams
        self.duration = duration

    @property
    def required_quantity(self):
        original_value = self.duration * self.total_per_day
        new_value = int(round(original_value))
        return new_value if (
            new_value > original_value) else int(round(original_value)) + 1

    @property
    def dose(self):
        """Returns required dosage by weight in milligrams.
        For Example
            4mg/kg means give 4mg for every kg the person weighs.
            A 75 kg person would need 75 x 4 = 300mg."""
        return self.weight * self.dosage

    @property
    def formula(self):
        return self.dose / self.total

    @property
    def total_per_day(self):
        return (self.formula * 1)

    @property
    def __repr__(self):
        return f'{self.definition.description}'
