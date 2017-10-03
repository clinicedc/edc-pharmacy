from django.apps import apps as django_apps

from ..dispense.labels import DispenseLabel

from ..models.dispense_timepoint import DispenseTimepoint

edc_pharma_app_config = django_apps.get_app_config('edc_pharma')


class Dispense:

    """Print dispense labels and update dispense history.
    """
    print_label_cls = DispenseLabel

    def __init__(self, subject_identifier=None, timepoint_id=None):
        self.subject_identifier = subject_identifier
        self.timepoint_id = timepoint_id
        self.print_labels()

    @property
    def dispense_timepoint(self):
        """Returns dispense timepoint."""
        return DispenseTimepoint.objects.get(
            schedule__subject_identifier=self.subject_identifier,
            id=self.timepoint_id)

    def print_labels(self):
        """Print labels using dispense profile. """
        self.print_label_cls(
            dispense_timepoint=self.dispense_timepoint,
            copies=1, template_name=edc_pharma_app_config.template_name)


# 092-40990001-3
# ''
