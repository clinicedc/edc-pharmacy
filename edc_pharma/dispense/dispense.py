from django.apps import apps as django_apps

from edc_pharma.dispense.labels.print_label import PrintLabel

from ..models.dispense_timepoint import DispenseTimepoint

edc_pharma_app_config = django_apps.get_app_config('edc_pharma')


class Dispense:

    """Print dispense labels and update dispense history.
    """
    print_label_cls = PrintLabel

    def __init__(self, subject_identifier=None, timepoint=None):
        self.subject_identifier = subject_identifier
        self.timepoint = timepoint

    @property
    def dispense_timepoint(self):
        """Returns dispense timepoint."""
        return DispenseTimepoint.objects.get(
            schedule__subject_identifier=self.subject_identifier,
            timepoint=self.timepoint)

    def print_labels(self):
        """Print labels using dispense profile. """
        self.print_label_cls(
            dispense_timepoint=self.dispense_timepoint,
            copies=1, template_name=edc_pharma_app_config.template_name)
