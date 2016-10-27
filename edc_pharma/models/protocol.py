from django.db import models
from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel


class Protocol(BaseUuidModel):

    history = HistoricalRecords()

    number = models.CharField(max_length=30)

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.number
