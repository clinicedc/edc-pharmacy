from django.db import models
from django.utils import timezone
from edc_base.model.models import BaseUuidModel


class Protocol(BaseUuidModel):
    protocol_number = models.CharField(max_length=30)
    protocol_name = models.CharField(max_length=200)

    def __str__(self):
        return self.protocol_name


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
    medium = models.CharField(max_length=50)
    storage_instructions = models.TextField(max_length=200)

    def __str__(self):
        return self.treatment_name


class Dispense(BaseUuidModel):
    patient = models.ForeignKey(Patient)
    treatment = models.ForeignKey(Treatment)
    dose_amount = models.CharField(max_length=20)
    frequency_per_day = models.IntegerField()
    date_prepared = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.patient.subject_identifier
    
    
class PrintSave(models.Model):
    def next(self):
        try:
            return PrintSave.objects.save()
        except:
            return None
