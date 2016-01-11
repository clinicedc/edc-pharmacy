from edc.core.identifier.models import BaseSequence


class IdentifierSequence(BaseSequence):

    class Meta:
        app_label = "dispenser"
        db_table = "ph_dispenser_identifier_sequence"
