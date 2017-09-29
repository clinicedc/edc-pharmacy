from django.db import models

from edc_base.model_mixins import BaseUuidModel


class DispenseSchedule(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=150,)

    name = models.CharField(max_length=100,)

    sequence = models.IntegerField()

    duration = models.CharField(max_length=100,)

    description = models.CharField(max_length=100,)

    start_date = models.DateField()

    end_date = models.DateField()

    class Meta:
        app_label = 'edc_pharma'
