from edc_pharma.constants import CAPSULE

from .capsule_dosage import CapsuleDosage
from .vial_dosage import VialDosage


class Medication:
    """Given a medication definition and subject weight the class calculates the 
    quantity of medication or the volume to dispense.
    For Example.
        Amphotericin B
        weight = 32kg, unit=1mg, category=vial, amount=50, duration = 7 days
        Number of Dispenses/vial size in mg = (weight * unit * duration) / amount

    """

    capsule_dosage_cls = CapsuleDosage
    vial_dosage_cls = VialDosage

    def __init__(self, medication_definition=None, weight=None, duration=None):
        self.definition = medication_definition
        self.weight = weight
        self.duration = duration

    @property
    def required_quantity(self):
        result = None
        if self.definition == CAPSULE:
            result = self.capsule_dosage_cls(
                weight=self.weight, total=self.definition.total,
                millgrams=self.definition.milligram,
                duration=self.duration)
        else:
            result = self.vial_dosage_cls(
                weight=self.weight, total=self.definition.total,
                millgrams=self.definition.milligram,
                duration=self.duration)
        return result.required_quantity

    def __repr__(self):
        return f'{self.definition.description}'
