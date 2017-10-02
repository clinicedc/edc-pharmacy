

class DispenseLabelInstruction:

    """Returns the instructions for the dispensed medications.
    """

    def __dict__(self, dispense_timepoint=None, medication=None):
        self.dispense_timepoint = dispense_timepoint
        self.medication = medication

    @property
    def instruction(self):
        pass
