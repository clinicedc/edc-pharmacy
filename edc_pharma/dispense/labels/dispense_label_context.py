from django.apps import apps as django_apps

edc_pharma_app_config = django_apps.get_app_config('edc_pharma')


class DispenseLabelContext:
    """Format dispense record into printable ZPL label context."""

    def __init__(self, dispense_appointment=None):
        self.dispense_appointment = dispense_appointment

    @property
    def context(self):
        # FIXME, request for print label from the ambition team.
        subject_identifier = self.dispense_appointment.schedule.subject_identifier
        return {
            'barcode_value': subject_identifier,
            'site': edc_pharma_app_config.site_code,
            'telephone_number': None,
            'patient': None,
            'medication': None,
            'clinician_initials': None,
            'number_of_tablets': None,
            'times_per_day': None,
            'total_number_of_tablets': None,
            'storage_instructions': None,
            'sid': None,
            'prepared_datetime': self.dispense_appointment.timepoint.strftime(
                '%Y-%m-%d'),
            'subject_identifier': subject_identifier,
            'prepared_by': None,
            'protocol': None,
            'initials': None,
        }

    @property
    def context_list(self):
        context_list = []
        context = self.context
        for medication in self.dispense_appointment.profile_medications:
            context.update({
                'medication': medication.description})
            context_list.append(context)
        return context_list
