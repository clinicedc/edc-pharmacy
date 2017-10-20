from copy import deepcopy

from django.apps import apps as django_apps


edc_pharma_app_config = django_apps.get_app_config('edc_pharma')


class DispenseLabelContext:
    """Format dispense record into printable ZPL label context."""

    def __init__(self, prescriptions=None):
        self.prescriptions = prescriptions

    def context(self, prescription):
        # FIXME, request for print label from the ambition team.
        subject_identifier = prescription.subject_identifier
        category = prescription.category
        return {
            'barcode_value': subject_identifier,
            'site': edc_pharma_app_config.site_code,
            'telephone_number': None,
            'medication': prescription.description,
            'clinician_initials': None,
            'number_of_tablets': None,
            'times_per_day': None,
            'total_number_of_tablets': f'{prescription.result} {category}',
            'storage_instructions': None,
            'prepared_datetime': prescription.modified.strftime(
                '%Y-%m-%d'),
            'subject_identifier': subject_identifier,
            'prepared_by': None,
            'protocol': None,
            'initials': None,
        }

    @property
    def context_list(self):
        context_list = []
        for medication in self.self.prescriptions:
            context = self.context(medication)
            context_list.append(context)
        return context_list
