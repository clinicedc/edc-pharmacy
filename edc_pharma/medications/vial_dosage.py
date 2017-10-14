from .drug_mixin import DrugMixin


class VialDosage(DrugMixin):
    """
    Calculates drug dosage for vials.
    """

    def __init__(self, body_weight=None, strength_of_vial=None,
                 millgrams_per_vial=None, duration=None):
        self.body_weight = body_weight
        self.strength_of_vial = strength_of_vial
        self.millgrams_per_vial = millgrams_per_vial
        self.duration = duration

    @property
    def daily_dosage(self):
        """Returns dosage per day."""
        daily_dosage = ((self.millgrams_per_vial * self.body_weight) /
                        self.strength_of_vial)
        return round(daily_dosage)

    @property
    def __repr__(self):
        return f'{self.definition.description}'
