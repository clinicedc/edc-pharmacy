from datetime import datetime


from django.core.exceptions import ObjectDoesNotExist

from ..models import Medication
from ..models.dispense_history import DispenseHistory


class DispenseHistoryCreator:
    """Creates dispense history record after printing the labels."""

    def __init__(self, dispense_appointment=None):
        self.dispense_appointment = dispense_appointment

    def create_or_update(self):
        model_obj = self.dispense_history
        model_obj.save()
        for medication in self.dispense_appointment.profile_medications:
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
        self.dispense_appointment.is_dispensed = True
        self.dispense_appointment.save()

    @property
    def dispense_history(self):
        try:
            dispense_history = DispenseHistory.objects.get(
                dispense_appointment=self.dispense_appointment
            )
        except DispenseHistory.DoesNotExist:
            dispense_history = DispenseHistory(
                dispense_appointment=self.dispense_appointment,
                dispense_datetime=datetime.today()
            )
        return dispense_history
