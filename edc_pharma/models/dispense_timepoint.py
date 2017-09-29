from django.db import models

from edc_base.model_mixins import BaseUuidModel
from .dispense_schedule import DispenseSchedule


class DispenseTimepoint(BaseUuidModel):

    timepoint = models.DateField()

    is_dispensed = models.BooleanField(default=False)

    schedule = models.ForeignKey(DispenseSchedule)

    profile_label = models.CharField(max_length=100)

    class Meta:
        app_label = 'edc_pharma'
