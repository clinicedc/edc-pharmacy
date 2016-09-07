from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel

TABLET = 'TABLET'
SYRUP = 'SYRUP'
DISPENSE_TYPES = (
    (TABLET, 'Tablet'),
    (SYRUP, 'Syrup'),
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
        return '{} ({}) Site {}'.format(self.subject_identifier, self.initials, self.site.site_code)


class Treatment(BaseUuidModel):

    name = models.CharField(max_length=50)

    protocol = models.ForeignKey(Protocol)

    storage_instructions = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Dispense(BaseUuidModel):

    patient = models.ForeignKey(Patient)

    treatment = models.ForeignKey(Treatment)

    dispense_type = models.CharField(
        max_length=8,
        choices=DISPENSE_TYPES,
        default=TABLET)

    number_of_tablets_or_teaspoons = models.CharField(max_length=5)

    times_per_day = models.CharField(max_length=3)

    total_number_of_tablets = models.CharField(blank=True, max_length=5)

    total_dosage_volume = models.CharField(blank=True, max_length=10)

    prepared_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.patient)
