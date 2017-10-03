from edc_label.label import Label
from edc_pharma.dispense.dispense_history_creator import DispenseHistoryCreator

from .dispense_label_context import DispenseLabelContext


class DispenseLabel:
    """Print medication label given dispense timepoint record.
    """
    label_cls = Label
    label_context_cls = DispenseLabelContext
    dispense_history_creator_cls = DispenseHistoryCreator
    template_name = 'dispense'

    def __init__(self, dispense_timepoint=None, copies=None, template_name=None):
        self.copies = copies or 1
        self.dispense_timepoint = dispense_timepoint
        self.label = self.label_cls(
            template_name=template_name or self.template_name)

        self.context_list = self.label_context_cls(
            dispense_timepoint=self.dispense_timepoint).context_list
        self.print_labels()

    def print_labels(self):
        for context in self.context_list or []:
            self.label.print_label(copies=self.copies, context=context)
            dispense_creator = self.dispense_history_creator_cls(
                dispense_timepoint=self.dispense_timepoint)
            dispense_creator.save_or_update()
