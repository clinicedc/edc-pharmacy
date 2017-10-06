from django.apps import apps as django_apps

from ..dispense.labels import DispenseLabel

from ..models.dispense_appointment import DispenseAppointment

edc_pharma_app_config = django_apps.get_app_config('edc_pharma')


class Dispense:

    """Print dispense labels and update dispense history.
    """
    print_label_cls = DispenseLabel

    def __init__(self, subject_identifier=None, timepoint_id=None,
                 user=None):
        self.subject_identifier = subject_identifier
        self.timepoint_id = timepoint_id
        self.user = user
        self.printed_labels = self.print_labels()

    @property
    def dispense_appointment(self):
        """Returns dispense timepoint."""
        return DispenseAppointment.objects.get(
            schedule__subject_identifier=self.subject_identifier,
            id=self.timepoint_id)

    def print_labels(self):
        """Print labels using dispense profile. """
        printer = self.print_label_cls(
            dispense_appointment=self.dispense_appointment,
            copies=1, template_name=edc_pharma_app_config.template_name)
        return printer.print_labels
