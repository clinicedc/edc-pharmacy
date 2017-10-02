from edc_label.label import Label
from edc_pharma.dispense.dispense_history_creator import DispenseHistoryCreator

from .label_context import LabelContext


class PrintLabel:
    """Print medication label given dispense timepoint record.
    """
    label_cls = Label
    label_context_cls = LabelContext
    dispense_history_creator_cls = DispenseHistoryCreator

    def __init__(self, dispense_timepoint=None,
                 copies=None, template_name=None):
        self.copies = copies or 1
        self.dispense_timepoint = dispense_timepoint
        self.label = self.label_cls(
            template_name=template_name)

        self.context_list = self.label_context_cls(
            dispense_timepoint=self.dispense_timepoint).context_list

    def print_label(self):
        for context in self.context_list or []:
            self.label.print_label(copies=self.copies, context=context)
            self.dispense_history_creator_cls(
                dispense_timepoint=self.dispense_timepoint,
                context=context)
