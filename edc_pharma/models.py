from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel

TABLET = 'TABLET'
SYRUP = 'SYRUP'
IV = 'IV'
DISPENSE_TYPES = (
    (TABLET, 'TABLET'),
    (SYRUP, 'SYRUP'),
    (IV, 'IV'),
)


class Protocol(BaseUuidModel):

    number = models.CharField(max_length=30)

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.number


class Site(BaseUuidModel):

    protocol = models.ForeignKey(Protocol)

    site_code = models.CharField(max_length=20)

    telephone_number = models.CharField(max_length=7)

    def __str__(self):
        return self.site_code


class Patient(BaseUuidModel):

    subject_identifier = models.CharField(max_length=20)

    initials = models.CharField(max_length=5)

    sid = models.CharField(max_length=20)

    consent_datetime = models.DateTimeField(default=timezone.now)

    site = models.ForeignKey(Site)

    def __str__(self):
        return '{}, ({}), Site {}'.format(self.subject_identifier, self.initials, self.site.site_code)


class Medication(BaseUuidModel):

    name = models.CharField(max_length=200)

    protocol = models.ForeignKey(Protocol)

    storage_instructions = models.TextField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'edc_pharma'


class Dispense(BaseUuidModel):

    patient = models.ForeignKey(Patient)

    medication = models.ForeignKey(Medication, default=None)

    dispense_type = models.CharField(
        max_length=8,
        choices=DISPENSE_TYPES,
        default=TABLET
    )

    number_of_tablets = models.IntegerField(blank=True, null=True, help_text="Only required if dispense type TABLET is chosen")

    number_of_teaspoons = models.IntegerField(blank=True, null=True, help_text="Only required if dispense type SYRUP is chosen")

    times_per_day = models.IntegerField(default=3)

    total_number_of_tablets = models.IntegerField(blank=True, null=True, help_text="Only required if dispense type TABLET is chosen")

    total_dosage_volume = models.CharField(max_length=10, blank=True, null=True, help_text="Only required if dispense type SYRUP or IV is chosen")

    iv_duration = models.CharField(max_length=15, blank=True, null=True, help_text="Only required if dispense type IV is chosen")

    prepared_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.patient.subject_identifier

    @property
    def label_context(self):
        label_context = {
            'site': self.patient.site,
            'telephone_number': self.patient.site.telephone_number,
            'patient': self.patient.subject_identifier,
            'initials': self.patient.initials,
            'sid': self.patient.sid,
            'times_per_day': self.times_per_day,
            'drug_name': self.medication,
            'date_prepared': self.prepared_datetime.date(),
            'drug_name': self.medication,
            'prepared_datetime': self.prepared_datetime.date(),
            'prepared_by': self.user_created,
            'storage_instructions': self.medication.storage_instructions,
            'protocol': self.medication.protocol,
        }
        if self.dispense_type == TABLET:
            label_context.update({
                'number_of_tablets': self.number_of_tablets,
                'total_tablets_dispensed': self.total_number_of_tablets,
            })
        elif self.dispense_type == SYRUP:
            label_context.update({
                'number_of_teaspoons': self.number_of_teaspoons,
                'quantity_dispensed': self.total_dosage_volume,
            })
        return label_context

    class Meta:
        unique_together = (('patient', 'medication', 'prepared_datetime'), )


class PrintSave(models.Model):
    def next(self):
        try:
            return PrintSave.objects.save()
        except:
            return None
