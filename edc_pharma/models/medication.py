from edc_base.model_mixins import ListModelMixin, BaseUuidModel

from django.db import models


class Medication(ListModelMixin, BaseUuidModel):

    description = models.CharField(
        max_length=250,)

    storage_instructions = models.TextField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'edc_pharma'
