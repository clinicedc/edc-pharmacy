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
    site_number = models.CharField(max_length=20)
    telephone_number = models.CharField(max_length=7)

    def __str__(self):
        return self.site_number


class Patient(BaseUuidModel):
    subject_identifier = models.CharField(max_length=20)
    initials = models.CharField(max_length=5)
    sid = models.CharField(max_length=20)
    consent_datetime = models.DateTimeField(default=timezone.now)
    site = models.ForeignKey(Site)

    def __str__(self):
        return self.subject_identifier


class Medication(BaseUuidModel):
    name = models.CharField(max_length=50, unique=True)
    protocol = models.ForeignKey(Protocol)
    storage_instructions = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Dispense(BaseUuidModel):
    patient = models.ForeignKey(Patient)
    medication = models.ForeignKey(Medication)
    dispense_type = models.CharField(
        max_length=8,
        choices=DISPENSE_TYPES,
        default=TABLET
    )
    number_of_tablets_or_teaspoons = models.IntegerField(default=1)
    times_per_day = models.IntegerField(default=3)
    total_number_of_tablets = models.IntegerField(default=30, blank=True)
    total_dosage_volume = models.CharField(max_length=10, blank=True)
    iv_duration = models.CharField(max_length=15)
    prepared_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.patient.subject_identifier

    class Meta:
        unique_together = (('patient', 'medication', 'prepared_datetime'), )
