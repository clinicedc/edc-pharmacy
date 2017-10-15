from datetime import datetime
from edc_pharma.medications import medications

from django.core.exceptions import ObjectDoesNotExist

from ..models import MedicationDefinition
from ..models.dispense_history import DispenseHistory


class DispenseHistoryCreator:
    """Creates dispense history record after printing the labels."""

    def __init__(self, dispense_appointment=None, selected=None, medication_name=None):
        self.medication_name = medication_name
        self.dispense_appointment = dispense_appointment
        self.selected = selected

    def create_all(self):
        """Create history record per medication and update the next dispense appt.
        """
        if self.selected:
            medication_definition = medications.get(self.medication_name)
            self.create_history(medication_definition=medication_definition)
        else:
            for medication_definition in self.dispense_appointment.profile_medications:
                self.create_history(
                    medication_definition=medication_definition)
        self.dispense_appointment.update_next_dispense_datetime()

    def medication(self, medication_definition=None):
        try:
            medication_obj = MedicationDefinition.objects.get(
                name=medication_definition.name,
                description=medication_definition.description)
        except ObjectDoesNotExist:
            medication_obj = MedicationDefinition.objects.create(
                name=medication_definition.name,
                unit=medication_definition.unit,
                category=medication_definition.category,
                description=medication_definition.description)
        return medication_obj

    def create_history(self, medication_definition=None):

        medication_obj = self.medication(
            medication_definition=medication_definition)
        model_obj = self.dispense_history(
            medication_definition=medication_obj)
        model_obj.save()

    def save_or_update(self):
        self.create_all()
        self.dispense_appointment.is_dispensed = True
        self.dispense_appointment.save()

    def dispense_history(self, medication_definition=None):
        try:
            dispense_history = DispenseHistory.objects.get(
                dispense_appointment=self.dispense_appointment,
                medication_definition=medication_definition
            )
        except DispenseHistory.DoesNotExist:
            dispense_history = DispenseHistory(
                dispense_appointment=self.dispense_appointment,
                dispense_datetime=datetime.today(),
                medication_definition=medication_definition
            )
        return dispense_history
