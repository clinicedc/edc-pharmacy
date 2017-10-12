from edc_pharma.constants import CAPSULE

from .capsule_formula import CapsuleFormula
from .medication_definition import MedicationDefinition
from .vial_formula import VialFormula


class Medication:
    """Given a medication and subject weight the class calculates the 
    quantity of medication or the volume to dispense.
    For Example.
        Amphotericin B
        weight = 32kg, unit=1mg, category=vial, amount=50, duration = 7 days
        Number of Dispenses/vial size in mg = (weight * unit * duration) / amount

    """

    vial_formula_cls = VialFormula
    capsule_formula_cls = CapsuleFormula

    def __init__(self, medication_definition=None, weight=None, duration=None):
        self.definition = medication_definition
        self.weight = weight
        self.duration = duration

    @property
    def total(self):
        result = None
        if self.definition == CAPSULE:
            result = self.capsule_formula(
                weight=self.weight, med_weight=self.definition.weight,
                millgrams=self.definition.milligram,
                duration=self.duration)
        else:
            result = self.vial_formula_cls(
                weight=self.weight, med_weight=self.definition.weight,
                millgrams=self.definition.milligram,
                duration=self.duration)
        return result.total

    def __repr__(self):
        return f'{self.definition.description}'
