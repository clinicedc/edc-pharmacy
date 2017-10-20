from django.apps import apps as django_apps

from ..constants import PRINT_SELECTED
from ..dispense.labels import DispenseLabel
from ..models import DispenseAppointment, Prescription


edc_pharma_app_config = django_apps.get_app_config('edc_pharma')


class Dispense:

    """Print dispense labels and update dispense history.
    """
    print_label_cls = DispenseLabel

    def __init__(self, subject_identifier=None, appointment_id=None,
                 user=None, prescriptions=None, action=None):
        self.subject_identifier = subject_identifier
        self.appointment_id = appointment_id
        self._prescriptions = prescriptions
        self.user = user
        self.action = action
        self.printed_labels = self.print_labels()

    def prescriptions(self):
        if self.action == PRINT_SELECTED:
            return self._prescriptions
        else:
            return Prescription.objects.filter(
                dispense_appointment__id=self.appointment_id)

    @property
    def dispense_appointment(self):
        """Returns dispense timepoint."""
        return DispenseAppointment.objects.get(
            schedule__subject_identifier=self.subject_identifier,
            id=self.appointment_id)

    def print_labels(self):
        """Print labels using dispense profile. """
        printer = self.print_label_cls(
            prescriptions=self.prescriptions,
            copies=1, template_name=edc_pharma_app_config.template_name)
        return printer.print_labels


class MedicationNotApprovedError(Exception):
    pass


class DispenseAction:

    def __init__(self, appointment_id=None):
        self.appointment_id = appointment_id
        dispense_appt = DispenseAppointment.objects.get(
            id=self.appointment_id)
        self.validate(appointment=dispense_appt)
        dispense_appt.is_dispensed = True
        dispense_appt.save()

    def validate(self, appointment=None):
        if Prescription.objects.filter(
                is_approved=False, dispense_apppointment=appointment):
            raise MedicationNotApprovedError(f'Meication not approved error! '
                                             'Please approved all medications '
                                             'before dispensing. ')
