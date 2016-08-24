from django.db import models
from django.utils import timezone

class Protocol(models.Model):
    protocol_number = models.CharField(max_length=30)
    protocol_name = models.CharField(max_length=200)


class Site(models.Model):
    protocol = models.ForeignKey(Protocol)
    site_number = models.IntegerField()
    telephone_number = models.CharField(max_length=7)


class Patient(models.Model):
    subject_identifier = models.CharField(max_length=20)
    initials = models.CharField(max_length=5)
    sid = models.CharField(max_length=20)
    consent_date = models.DateTimeField(default=timezone.now)
    site = models.ForeignKey(Site)


class Treatment(models.Model):
    treatment_name = models.CharField(max_length=50)
    protocol = models.ForeignKey(Protocol)
    medium = models.CharField(max_length=50)
    storage_instructions = models.CharField(max_length=200)


class Dispense(models.Model):
    patient = models.ForeignKey(Patient)
    treatment = models.ForeignKey(Treatment)
    dose_amount = models.CharField(max_length=20)
    frequency_per_day = models.IntegerField()
    date_prepared = models.DateTimeField(default=timezone.now)
    prepared_by = models.CharField (max_length=100)
    quantity_dispensed = models.CharField (max_length=20)
