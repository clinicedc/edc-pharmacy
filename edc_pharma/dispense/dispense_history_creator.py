from datetime import datetime

from edc_pharma.models.dispense_history import DispenseHistory
from edc_pharma.models.list_models import Medication


class DispenseHistoryCreator:
    """Creates dispense history record after printing the labels."""

    def __init__(self, dispense_timepoint=None):
        self.dispense_timepoint = dispense_timepoint

    def create_or_update(self):
        for medication in self.dispense_timepoint.profile_medications:
            try:
                self.dispense_history.medications.get(
                    name=medication.name)
            except Medication.DoesNotExist:
                self.dispense_history.medications.add(
                    medication)

    def save_or_update(self):
        self.create_or_update()
        self.validate()
        self.dispense_history.save()

    @property
    def dispense_history(self):
        try:
            self.dispense_history = DispenseHistory.objects.get(
                dispense_timepoint=self.dispense_timepoint
            )
        except DispenseHistory.DoesNotExist:
            self.dispense_history = DispenseHistory(
                dispense_timepoint=self.dispense_timepoint,
                dispense_datetime=datetime.today()
            )
