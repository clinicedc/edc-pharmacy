from django.db import models
from .dispense_schedule import DispenseSchedule


class DispenseryPlan(models.Model):

    subject_identifier = models.CharField(
        max_length=150,)

    timepoint = models.DateField()

    schedule = models.ForeignKey(DispenseSchedule)

    class Meta:
        app_label = 'edc_pharma'
