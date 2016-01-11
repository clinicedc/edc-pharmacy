from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from edc_base.model.models import BaseUuidModel
from edc_registration.models import RegisteredSubject
from ..classes import DispensingIdentifier
from ..choices import PACKING_UNITS


class Dispensing(BaseUuidModel):

    identifier = models.CharField(max_length=25, editable=False)
    registered_subject = models.ForeignKey(RegisteredSubject, null=True, editable=False)
    dispense_date = models.DateField(default=date.today())
    subject_identifier = models.CharField(max_length=25)
    initials = models.CharField(max_length=10)
    sid = models.CharField(max_length=10)
    packing_amount = models.IntegerField()
    packing_unit = models.CharField(
        max_length=25,
        choices=PACKING_UNITS)
    treatment = models.CharField(max_length=25)
    dose = models.CharField(max_length=25)
    copies = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
#         if not RegisteredSubject.objects.filter(subject_identifier=self.subject_identifier, sid=self.sid, initials=self.initials):
#             raise ValidationError('Subject not found. Using criteria {0}. Perhaps catch this in forms.py'.format((self.subject_identifier, self.sid, self.initials)))
        if not self.id:
            if not self.identifier:
                self.identifier = DispensingIdentifier().get_identifier()
        super(Dispensing, self).save(*args, **kwargs)

    def barcode_value(self):
        return self.identifier

    def __unicode__(self):
        return self.identifier

    class Meta:
        app_label = "dispenser"
        db_table = "ph_dispenser_dispensing"
