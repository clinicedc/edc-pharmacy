from edc_pharma.constants import CAPSULE


class DispenseMedQuantity:
    """Given a medication and subject weight the class calculates the 
    quantity of medication to dispense.
    For Example.
        Amphotericin B
        weight = 32kg, unit=1mg, category=vial, amount=50, duration = 7 days
        Number of Dispenses/vial size in mg = (weight * unit * duration) / amount

    """

    def __init__(self, medication=None, weight=None, duration=None):
        self.medication = medication
        self.weight = weight
        self.duration = duration

    @property
    def total_quantity(self):
        original_value = self.duration * self.quantity_per_day
        new_value = int(round(original_value))
        return new_value if (
            new_value > original_value) else int(round(original_value)) + 1

    @property
    def take(self):
        if self.medication.category == CAPSULE:
            return 2
        return 0

    @property
    def quantity_per_day(self):
        """Returns quantity of medication to dispenses. """
        return (self.weight * self.medication.volume) / self.medication.amount

    def __repr__(self):
        return f'{self.medication.description}'
