from datetime import datetime

from edc_pharma.models.dispense_history import DispenseHistory
from edc_pharma.models.list_models import Medication


class DispenseHistoryCreator:
    """Creates dispense history record after printing the labels."""

    def __init__(self, dispense_timepoint=None):
        self.dispense_timepoint = dispense_timepoint

    def create_or_update(self):
        model_obj = self.dispense_history
        model_obj.save()
        for medication in self.dispense_timepoint.profile_medications:
            try:
                model_obj.medications.get(name=medication.name)
            except Medication.DoesNotExist:
                model_obj.medications.create(**{'name': medication.name})

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
