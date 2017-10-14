from .drug_mixin import DrugMixin


class CapsuleDosage(DrugMixin):
    """
    Calculates drug dosage for capsules.
    """

    def __init__(self, body_weight=None, strength=None,
                 millgrams_per_vial=None, duration=None, use_body_weight=None):
        self.body_weight = body_weight
        self.strength = strength
        self.millgrams_per_vial = millgrams_per_vial
        self.duration = duration
        self.use_body_weight = use_body_weight

    @property
    def daily_dosage(self):
        """Returns dosage per day."""
        if self.use_body_weight:
            daily_dosage = ((self.millgrams_per_vial * self.body_weight) /
                            self.strength)
        else:
            daily_dosage = self.millgrams_per_vial / self.strength
        return round(daily_dosage)

    @property
    def __repr__(self):
        return f'{self.definition.description}'
