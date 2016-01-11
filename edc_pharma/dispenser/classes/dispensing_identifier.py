from edc_identifier.classes import BaseIdentifier


class DispensingIdentifier(BaseIdentifier):

    def __init__(self):
        app_name = 'dispenser'
        model_name = 'dispensingidentifiermodel'
        identifier_format = 'PH{identifier_prefix}{site_code}{device_id}{sequence}'
        site_code = 0
        sequence_app_label = 'dispenser'
        sequence_model_name = 'IdentifierSequence'
        super(DispensingIdentifier, self).__init__(identifier_format=identifier_format, app_name=app_name, model_name=model_name, site_code=site_code,
                                                   sequence_app_label=sequence_app_label, sequence_model_name=sequence_model_name)
