

class DispenseLabelContext:
    """Format dispense record into printable ZPL label context."""

    def __init__(self, dispense_timepoint=None):
        self.dispense_timepoint = dispense_timepoint

    @property
    def context(self):
        # FIXME, request for print label from the ambition team.
        subject_identifier = self.dispense_timepoint.schedule.subject_identifier
        return {
            'barcode_value': subject_identifier,
            'site': None,
            'clinician_initials': None,
            'timepoint': self.dispense_timepoint.timepoint.strftime(
                '%Y-%m-%d'),
            'subject_identifier': subject_identifier,
            'initials': None,
        }

    @property
    def context_list(self):
        context_list = []
        context = self.context
        for medication in self.dispense_timepoint.profile_medications:
            context.update({'name': medication.name,
                            'description': medication.description})
            context_list.append(context)
        return context_list
