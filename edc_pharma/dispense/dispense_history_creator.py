from datetime import datetime


from django.core.exceptions import ObjectDoesNotExist

from ..models import Medication
from ..models.dispense_history import DispenseHistory


class DispenseHistoryCreator:
    """Creates dispense history record after printing the labels."""

    def __init__(self, dispense_timepoint=None):
        self.dispense_timepoint = dispense_timepoint

    def create_or_update(self):
        model_obj = self.dispense_history
        model_obj.save()
        for medication in self.dispense_timepoint.profile_medications:
            try:
                medication_obj = Medication.objects.get(
                    name=medication.name,
                    description=medication.description)
            except ObjectDoesNotExist:
                medication_obj = Medication.objects.create(
                    name=medication.name,
                    description=medication.description,
                    storage_instructions=medication.instruction)
            model_obj.medications.add(medication_obj)

    def save_or_update(self):
        self.create_or_update()
        self.dispense_history.save()
        self.dispense_timepoint.is_dispensed = True
        self.dispense_timepoint.save()

    @property
    def dispense_history(self):
        try:
            dispense_history = DispenseHistory.objects.get(
                dispense_timepoint=self.dispense_timepoint
            )
        except DispenseHistory.DoesNotExist:
            dispense_history = DispenseHistory(
                dispense_timepoint=self.dispense_timepoint,
                dispense_datetime=datetime.today()
            )
        return dispense_history
