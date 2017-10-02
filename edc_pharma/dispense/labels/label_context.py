from edc_pharma.dispense.dispense_label_instruction import DispenseLabelInstruction


class LabelContext:
    """Format dispense record into printable ZPL label context."""

    dispense_label_instruction_cls = DispenseLabelInstruction

    def __init__(self, dispense_timepoint=None):
        self.dispense_timepoint = dispense_timepoint
        self.instruction = self.dispense_label_instruction_cls(
            dispense_timepoint=self.dispense_timepoint).instruction

    @property
    def context(self):
        # FIXME, request for print label from the ambition team.
        subject_identifier = self.dispense_timepoint.schedule.subject_identifier
        return {
            'barcode_value': subject_identifier,
            'site': None,
            'clinician_initials': None,
            'timepoint': self.dispense_timepoint.timepoint.strftime(
                '%Y-%m-%d %H:%M'),
            'subject_identifier': subject_identifier,
            'initials': None,
            'instruction': self.instruction
        }

    @property
    def context_list(self):
        context_list = []
        for medication in self.dispense_timepoint.profile_medications:
            context = self.context
            context.update({'name': medication.name,
                            'description': medication.description})
            context_list.append(context)
        return context
