from ..models.dispense_timepoint import DispenseTimepoint

from .dispense_history_creator import DispenseHistoryCreator
from .dispense_instruction import DispenseInstruction


class Dispense:

    """Print dispense labels and update dispense history.
    """
    dispense_instruction_cls = DispenseInstruction
    dispense_history_creator_cls = DispenseHistoryCreator
    print_label_cls = PrintLabel

    def __init__(self, subject_identifier=None, timepoint_id=None):
        self.subject_identifier = subject_identifier
        self.timepoint_id = timepoint_id

    def dispense_timepoint(self):
        """Returns dispense timepoint."""
        return DispenseTimepoint.objects.get(
            schedule__subject_identifier=self.subject_identifier,
            id=self.timepoint_id)

    def print_labels(self):
        """Print labels using dispense profile. """
        self.print_label_cls(label=None, label_data=self.label_data)
