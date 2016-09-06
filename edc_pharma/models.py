from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel
from django.contrib.admin.filters import ChoicesFieldListFilter


class Protocol(BaseUuidModel):
    protocol_number = models.CharField(max_length=30)
    protocol_name = models.CharField(max_length=200)

    def __str__(self):
        return self.protocol_number


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
    consent_date = models.DateTimeField(default=timezone.now)
    site = models.ForeignKey(Site)

    def __str__(self):
        return self.subject_identifier


class Treatment(BaseUuidModel):
    treatment_name = models.CharField(max_length=50)
    protocol = models.ForeignKey(Protocol)
    storage_instructions = models.TextField(max_length=200)

    def __str__(self):
        return self.treatment_name


class Dispense(BaseUuidModel):
    patient = models.ForeignKey(Patient)
    treatment = models.ForeignKey(Treatment)
    TABLET = 'TABLET'
    SYRUP = 'SYRUP'
    DISPENSE_TYPES = (
        (TABLET, 'TABLET'),
        (SYRUP, 'SYRUP'),
    )
    dispense_type = models.CharField(
        max_length=8,
        choices=DISPENSE_TYPES,
        default=TABLET
    )
    number_of_tablets_or_teaspoons = models.CharField(max_length=3)
    times_per_day = models.CharField(max_length=3)
    total_number_of_tablets = models.CharField(max_length=3)
    date_prepared = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.patient.subject_identifier
