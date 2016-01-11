
from lis.labeling.classes import ModelLabel
from lis.labeling.models import ZplTemplate


class DispensingLabel(ModelLabel):

    def prepare_label_context(self, **kwargs):
        dispensing = kwargs.get('instance')
        custom = {}
        custom.update({
            'barcode_value': dispensing.barcode_value(),
            'subject_identifier': dispensing.subject_identifier,
            'initials': dispensing.initials,
            'treatment': dispensing.treatment,
            'sid': dispensing.sid,
            'dose': dispensing.dose,
            'packing_amount': dispensing.packing_amount,
            'packing_unit': dispensing.packing_unit,
            'dispense_date': dispensing.dispense_date,
            'user_created': dispensing.user_created,
            })
        self.label_context.update(**custom)

    def __init__(self):
        super(DispensingLabel, self).__init__()
        label_template = 'dispensing'
        if not ZplTemplate.objects.get(name=label_template):
            template_string = ('^XA'
                        '^FO100,25^A0N,25^FDBotswana-Harvard Partnership - SID ${sid}^FS'
                        '^FO100,50^BY2.0^BCN,50,N,N,N'
                        '^BY^FD${barcode_value}^FS'
                        '^FO100,120^A0N,20^FD${barcode_value}^FS'
                        '^FO100,150^A0N,30^FD${subject_identifier} [${initials}]^FS'
                        '^FO100,180^A0N,30^FD${treatment}^FS'
                        '^FO100,210^A0N,30^FD${dose}^FS'
                        '^FO100,270^A0N,40^FD${packing_amount} ${packing_unit}^FS'
                        '^FO100,330^A0N,30^FDdispensed on ${dispense_date} by ${user_created}^FS'
                        '^XZ')
            self.zpl_template = ZplTemplate.objects.create(
                        name=label_template,
                        template=template_string)
        else:
            self.zpl_template = ZplTemplate.objects.get(name=label_template)
