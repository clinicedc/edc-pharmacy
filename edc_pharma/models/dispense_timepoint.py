from django.db import models

from .dispense_schedule import DispenseSchedule


class DispenseTimepoint(models.Model):

    timepoint = models.DateField()

    schedule = models.ForeignKey(DispenseSchedule)

    profile_label = models.CharField(max_length=100)

    class Meta:
        app_label = 'edc_pharma'
