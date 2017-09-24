from django.db import models

from simple_history.models import HistoricalRecords

from edc_base.model_mixins import BaseUuidModel


class Protocol(BaseUuidModel):

    number = models.CharField(max_length=30)

    name = models.CharField(max_length=200, unique=True)

    objects = models.Manager()

    history = HistoricalRecords()

    def __str__(self):
        return self.number

    class Meta:
        app_label = 'edc_pharma'
