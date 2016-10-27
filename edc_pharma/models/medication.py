from django.db import models
from simple_history.models import HistoricalRecords

from edc_base.model.models import BaseUuidModel

from edc_pharma.models.protocol import Protocol


class Medication(BaseUuidModel):

    name = models.CharField(max_length=200)

    protocol = models.ForeignKey(Protocol)

    storage_instructions = models.TextField(max_length=200)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'edc_pharma'
