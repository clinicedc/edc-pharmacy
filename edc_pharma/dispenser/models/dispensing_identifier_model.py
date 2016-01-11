from django.db import models
from edc.core.identifier.models import BaseIdentifierModel


class DispensingIdentifierModel(BaseIdentifierModel):

    objects = models.Manager()

    class Meta:
        app_label = "dispenser"
        db_table = "ph_dispenser_dispensing_identifier_model"
        ordering = ['-created']
